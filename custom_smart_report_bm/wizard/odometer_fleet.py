# -*- coding: utf-8 -*-
# Copyright (C) 2022 - TODAY, Jescalante@blueminds.cl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.addons.fleet.models.fleet_vehicle_model import FUEL_TYPES
import base64
import json
import requests
from urllib.request import urlretrieve
from urllib.parse import urlencode
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
from calendar import monthrange
from io import BytesIO
import base64
import xlwt
import re


class FleetVehicleOdometer(models.TransientModel):
    _name = 'odometer.fleet'

    vehicle_id = fields.Many2one('fleet.vehicle')
    partner_id = fields.Many2one('res.partner')
    

    def call_api_odometer(self):
        today = date.today()
        Odometer = self.env['fleet.vehicle.odometer']
        now = datetime.now()
        days_months = monthrange(now.year, now.month)[1] + 1
        
        
        for i in range(1,days_months):
            last_odometer = Odometer.search(
            [('vehicle_id', '=', self.vehicle_id.id), ('tag_ids', 'in', [2])], order='id desc',limit=1)
        
            self.export_odometer_dates(last_odometer,i)

    def export_odometer_dates(self, last_odometer,i):
        Odometer = self.env['fleet.vehicle.odometer']
        config = self.env['ir.config_parameter'].sudo()
        if not config.get_param('api_odometer'):
            raise UserError(
                'Operacion no permitida, contacte al Administrador para activar API TAG y Multas.')

        date_start = last_odometer.date + timedelta(i + 1)
        date_end = date_start + timedelta(1)

        url = str(config.get_param('odo_url')) + \
            str(config.get_param('odo_user')) + '?'
        license_plate = self.vehicle_id.license_plate[:-2] + "-" + self.vehicle_id.license_plate[4:6]
        params = {
            'token': config.get_param('odo_token'),
            'patente': license_plate,  # 'PYFV-59',
            'fecha1': str(date_start.strftime("%Y-%m-%d  %H:%M:%S")),
            'fecha2': str(date_end.strftime("%Y-%m-%d %H:%M:%S"))
        }
        metodo = []
        qstr = urlencode(params)
        print(json.dumps(params, indent=4, ensure_ascii=False))
        response = requests.post(url + qstr)
        if response.status_code != 200:
            pass

        dict_list = json.loads(response.text.encode('utf8'))
        if dict_list.get('status') != 0:
            pass

        ult_valor = last_odometer.value
        if dict_list.get('data'):
            for tag in dict_list.get('data'):
                valor = float(tag.get('odometro')) / 1000
                ult_valor +=  float(valor)
            
                vals_data = {
                    'vehicle_id': self.vehicle_id.id,
                    'date': tag.get('fecha'),
                    'value': ult_valor,
                    'tag_ids': [2],
                }
                Odometer.create(vals_data)
