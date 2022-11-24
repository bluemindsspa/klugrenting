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


class AgreementInh(models.Model):
    _inherit = 'agreement'

    
    product_id = fields.Many2one('product.product')
    vehicle_id = fields.Many2one('fleet.vehicle')
    deducible = fields.Float('deducible')
    deducible_robo = fields.Float('deducible robo')
    place_contract = fields.Integer('Plazo Contrato (Meses)')
    km_salida = fields.Integer('Kilometraje de Salida')
    km_devo = fields.Integer('Kilometraje de Devolución')
    km_mes = fields.Integer('Kilometros Mensuales Contratados')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_fin = fields.Date('Fecha Final')
    price_km_adi = fields.Float('Precio por KM Adicional', readonly=False,
        track_visibility='onchange')
    price = fields.Float('Precio Mensual', readonly=False,
        track_visibility='onchange')
    price_instalacion = fields.Float('Garantia', readonly=False, track_visibility='onchange')
    warranty = fields.Selection(
        selection=[
            ('tarjeta', 'Tarjeta Bancaria'),
            ('trans', 'Transferencia')],
        string='Forma de Pago Garantia',
        required=True)
    estanque_salida = fields.Selection(
        selection=[
            ('porcentaje_25', '25%'),
            ('porcentaje_50', '50%'),
            ('porcentaje_75', '75%'),('100', '100%')],
        string='Estanque de Salida',
        required=True)
    estanque_devo = fields.Selection(
        selection=[
            ('porcentaje_25', '25%'),
            ('porcentaje_50', '50%'),
            ('porcentaje_75', '75%'),('100', '100%')],
        string='Estanque de Devolución',
        required=False)
    



    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id.product_id:
            self.product_id = self.vehicle_id.product_id.id

    def agree_sale(self):
        if not self.inicio_fecha_alquiler or not self.fin_fecha_alquiler:
            raise UserError(_(
                'Disculpe, No se puede iniciar la orden de venta, \n \n  Porque no ha la fecha inicio y la fecha fin'))
        months = (
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
        "Diciembre")
        descuento = False
    
        total_multas = 0.0
        total_tags = 0.0
        total_kms = 0.0
        vehicle = self.env['fleet.vehicle'].sudo().search([('product_id', '=', self.product_id.id)])
        primero = True
        today = datetime.now().date() + relativedelta(days=1) # self.fecha_cobro
        numeracion = 1
        proporcional = True
        es_primero = 1
        
        month = months[self.fecha_inicio.month - 1]
        order_vals = {
            'partner_id': self.partner_id.id,
            
            'agreement_id': self.id,
            'date_order': datetime.now(),
            'validity_date': self.end_date,
            # 'user_id': self.user_id.id,
            'origin': self.name,
            'partner_dir_id': self.partner_id.id,
            'is_rental_order': True,
            #'tipo_rental_order': 'mensualidad',
            'agreement_id': self.id,
            'payment_term_id': self.payment_term_id.id,
            #'payment_method': self.payment_method.id,
            #'payment_deadline': self.payment_deadline.id,
            'inicio_fecha_alquiler': self.fecha_inicio,
            'fin_fecha_alquiler': self.fecha_fin,
            'fecha_estimada': today,
            'fecha_fact_prog': today,
            'next_action_date': today,
            'periodo_mes': str(month) + '/' + str(self.fecha_fin.year)
        }
        order = self.env['sale.order'].create(order_vals)
        # name_order = str(order.name) + ' ' + str(today) + ' - ' + str(numeracion)
        # order.write({'name': name_order})
        # today = today + relativedelta(months=time_periodicy)
        order_line = {
            'order_id': order.id,
            'product_id': self.product_id.id,
            'name': 'Renting ' + str(month) + ' ' + str(self.product_id.name),
            'price_unit': self.price,
            'tax_id': [self.tax_id.id],
        }
        order_line = self.env['sale.order.line'].create(order_line)
        # Nota de Cobro
        init_anterior = self.fecha_inicio - relativedelta(months=1)
        ultimo_de_mes = calendar.monthrange(init_anterior.year, init_anterior.month)
        end_anterior = str(init_anterior.year) + '-' + str(init_anterior.month).zfill(2) + '-' + str(ultimo_de_mes[1])
        km_end_anterior = 0
        promedio_km = 0
        co2_e = 0
        co2_a = 0
        odometer_anterior = self.env['fleet.vehicle.odometer'].sudo().search([
                    ('vehicle_id', '=', vehicle.id),
                    ('date', '>=', init_anterior),
                    ('date', '<=', end_anterior),
                    ('tag_ids', 'in', [2])], order='id asc')
        if odometer_anterior:
            end = odometer_anterior[0].value
            # for mes in odometer_mes:
            #     km_end_anterior =abs(end - mes.value)
        odometer_mes = self.env['fleet.vehicle.odometer'].sudo().search([
            ('vehicle_id', '=', vehicle.id),
            ('date', '>=', self.fecha_inicio),
            ('date', '<=', self.fecha_fin),
            ('tag_ids', 'in', [2])], order='id asc')
        if odometer_mes:
            init = odometer_mes[0].value
            for mes in odometer_mes:
                total_kms =abs(init - mes.value)
            if total_kms > 0:
                promedio_km = total_kms / (float(self.place_contract) - 1)
        if vehicle.co2 > 0 and km_end_anterior > 0:
            co2_e = float(vehicle.co2) * km_end_anterior / 1000
        if vehicle.co2 > 0 and total_kms > 0:
            co2_a = total_kms * float(vehicle.co2) / 1000
        nota_line = {
            'order_id': order.id,
            'name': self.product_id.id,
            'code': self.product_id.patente,
            'km_anterior': km_end_anterior,
            'km_acum': total_kms,
            'km_mes': promedio_km,
            'mes_contract': int(self.place_contract) -1,
            'contract': self.place_contract,
            'co2_e': co2_e,
            'co2_a': co2_a,
        }
        self.env['sale.order.detail'].create(nota_line)
        # Detalle Nota de Cobro
        odometer_det = self.env['fleet.vehicle.odometer'].sudo().search([
            ('vehicle_id', '=', vehicle.id),
            ('date', '>=', self.fecha_inicio),
            ('date', '<=', self.fecha_fin),
            ('tag_ids', 'in', [1])])
        for detalle in odometer_det:
            nota_line = {
                'order_id': order.id,
                'name': self.product_id.id,
                'date': detalle.date,
                'concesion': detalle.concession,
                'description': detalle.description,
                'category': detalle.category,
                #'km': 1,
                'tarifa': detalle.amount,
            }
            self.env['sale.order.detaill'].create(nota_line)
        # kms Extra
        total = 0.0
        if total_kms > self.km_mes:
            total = total_kms - self.km_mes
            total = total * self.price_km_adi
        if total > 0:
            kms_line = {
                'order_id': order.id,
                'product_id': self.product_id.id,
                'name': "KM'S Extra " + str(self.product_id.patente) + " '" + str(month) + "' " + str(
                    self.price_km_adi) + str(self.currency_id_km.symbol) + " por kilometro adicional " + str(
                    total_kms) + "KM sobre " + str(
                    self.km_mes),
                'price_unit': total,
                'tax_id': [self.tax_id.id],
            }
            self.env['sale.order.line'].create(kms_line)
        # tags
        odometer_tag = self.env['fleet.vehicle.odometer'].sudo().search([
            ('vehicle_id', '=', vehicle.id),
            ('date', '>=', self.fecha_inicio),
            ('date', '<=', self.fecha_fin),
            ('tag_ids', 'in', [1])])
        if odometer_tag:
            for tag in odometer_tag:
                total_tags = float(total_tags) + float(tag.amount)
            tags_line = {
                'order_id': order.id,
                'product_id': self.product_id.id,
                'name': 'TAG ' + str(month) + ' ' + str(self.product_id.patente),
                'price_unit': total_tags,
                'tax_id': [self.tax_id.id],
            }
            self.env['sale.order.line'].create(tags_line)
        # multas
        odometer_multas = self.env['fleet.vehicle.odometer'].sudo().search([
            ('vehicle_id', '=', vehicle.id),
            ('date', '>=', self.fecha_inicio),
            ('date', '<=', self.fecha_fin),
            ('tag_ids', 'in', [7])])
        if odometer_multas:
            for multa in odometer_multas:
                total_multas = float(total_multas) + float(multa.amount)
            multas_line = {
                'order_id': order.id,
                'product_id': self.product_id.id,
                'name': 'Multas ' + str(month) + ' ' + str(self.product_id.patente),
                'price_unit': total_multas,
                'tax_id': [self.tax_id.id],
            }
            self.env['sale.order.line'].create(multas_line)
        return True
        
        