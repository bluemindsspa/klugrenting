# © 2022 (Jamie Escalante <jescalante@blueminds.cl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _
import base64
import logging
from io import BytesIO
from xlwt import Workbook, easyxf
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import time
from datetime import timedelta, datetime
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'
    
    
    
    
    # product_id = fields.Many2one('product.product')
    # vehicle_id = fields.Many2one('fleet.vehicle')
    deducible = fields.Float('deducible')
    deducible_robo = fields.Float('deducible robo')
    # place_contract = fields.Integer('Plazo Contrato (Meses)')
    # km_salida = fields.Integer('Kilometraje de Salida')
    # km_devo = fields.Integer('Kilometraje de Devolución')
    # km_mes = fields.Integer('Kilometros Mensuales Contratados')
    # fecha_inicio = fields.Date('Fecha Inicio')
    # fecha_fin = fields.Date('Fecha Final')
    # price_km_adi = fields.Float('Precio por KM Adicional', readonly=False,
    #     track_visibility='onchange')
    # price = fields.Float('Precio Mensual', readonly=False,
    #     track_visibility='onchange')
    # price_instalacion = fields.Float('Garantia', readonly=False, track_visibility='onchange')
    # warranty = fields.Selection(
    #     selection=[
    #         ('tarjeta', 'Tarjeta Bancaria'),
    #         ('trans', 'Transferencia')],
    #     string='Forma de Pago Garantia',
    #     required=True)
    # estanque_salida = fields.Selection(
    #     selection=[
    #         ('full', 'Lleno'),
    #         ('3/4', '3/4'),
    #         ('1/2', '1/2'),('1/4', '1/4')],
    #     string='Estanque de Salida',
    #     required=True)
    # estanque_devo = fields.Selection(
    #     selection=[
    #         ('full', 'Lleno'),
    #         ('3/4', '3/4'),
    #         ('1/2', '1/2'),('1/4', '1/4')],
    #     string='Estanque de Devolución',
    #     required=False)
    maintenance = fields.Char(string="Frecuencia de mantenimiento")
    
    
