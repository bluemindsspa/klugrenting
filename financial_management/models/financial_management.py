# © 2022 (Daniel Fernandez <daniel@klugrenting.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _

import ast
import json


class FinancialManagement(models.Model):
    _name = 'financial.management'
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char('id')
    entidad_general = fields.Many2one('res.partner', string='Entidad')
    entidad = fields.Many2one('res.partner', 'id de credito')
    tipo = fields.Many2one('type.credit', string='Tipo de Credito')
    cuota = fields.Integer()
    cuotas_totales = fields.Integer()
    inicio_credito = fields.Datetime()
    vencimiento_credito = fields.Datetime()
    compania = fields.Many2one('res.company')

    garantia = fields.Char()
    estado_de_pago = fields.Selection(
        [('nuevo', 'Nuevo'),('vigente', 'Vigente'), ('terminado', 'Terminado')], default='vigente', string='Estado')
    tasa_de_interes = fields.Float()  # formulario

    monto_seguro = fields.Integer()
    comision_credito = fields.Integer()
    notaria = fields.Integer()
    impuestos = fields.Integer()
    valor_inversion = fields.Integer()
    costo_total_credito = fields.Integer()
    cae = fields.Float()  # percentage formula del cae
    hide_boolean = fields.Boolean(default=False)

    notas = fields.Text()  # anotar cosas
    ultima_fecha_pago = fields.Datetime()
    ultimo_pago = fields.Integer()
    total_pagados = fields.Integer()
    plazo_inversion = fields.Char()
    saldo_capital_actual = fields.Integer()
    financial_lines_id = fields.One2many(
        'financial.management.line', 'financial_id')

    # @api.depends()
    # def _compute_valor_inversion(self):
    #     if self.monto_seguro or self.comision_credito:
    #         self.valor_inversion = self.costo_total_credito - self.monto_seguro - self.comision_credito
    #     else:
    #         self.valor_inversion = self.costo_total_credito

       
            

    @api.onchange('entidad')
    def _onchange_entidad(self):

        for record in self:
            self.write({'financial_lines_id': [(6, 0, [])]})
            if self.entidad:
                
                self.entidad_general = self.entidad.entidad_bancaria
                total_credito = 0
                total_inversion = 0
                accounts = []
            
                
                account_move_ids = self.env['account.move'].search(
                    [('partner_id', '=', self.entidad.id), ('journal_id', '=', 18)], order='invoice_date asc')
                
                # if self.financial_lines_id:
                #         accounts = self.financial_lines_id.mapped(
                #             'account_id').ids
                for acc in account_move_ids:
                    vals = {}
                    credito = 0
                    interes = 0
                    self.cuotas_totales = len(self.financial_lines_id) + 1

                    for line in acc.invoice_line_ids:
                        if line.product_id.id == 301:
                            credito += line.price_unit
                        if line.product_id.id == 287:
                            interes += line.price_unit

                    total_credito += credito + interes
                    total_inversion += credito

                    
                    # if acc.id not in accounts:

                    self.write({'financial_lines_id': [(0, 0, {
                        'financial_id': self.id,
                        'account_id': acc.id,
                        'fecha_pago': json.loads(acc.invoice_payments_widget)['content'][0]['date'] if acc.payment_state == 'paid' else False,
                        'fecha_vencimiento_pago': acc.invoice_date_due,
                        'capital': credito,
                        'interes': interes,
                        'pagado': True if acc.payment_state == 'paid' else False,
                        'valor_cuota': credito + interes
                        # 'saldo_capital': total_inversion
                    })]})

                
                self.costo_total_credito = total_credito
                
                #self.count_saldo_capital()

    def count_saldo_capital(self):
        
        self.valor_inversion = self.costo_total_credito - self.monto_seguro - self.comision_credito - self.impuestos - self.notaria
        # for record in self.financial_lines_id:
        #     prueba = self.valor_inversion
            
            # record.saldo_capital -= prueba
            # record.saldo_capital = abs (record.saldo_capital)
        self.cron_change_values()
        self.hide_boolean = True
    
    def cron_change_values(self):
        
        credits_ids = self.env['financial.management'].search([])
        
        for record in credits_ids:
            record.cuota = 0
            for line in record.financial_lines_id:
                line.pagado = True if line.account_id.payment_state == 'paid' else False
                if line.pagado:
                    record.cuota += len(line)
                    
                    record.ultima_fecha_pago = line.fecha_pago
                    record.ultimo_pago = line.capital
                    record.total_pagados += line.capital
                    record.saldo_capital_actual = abs(line.saldo_capital)
            if record.cuota == record.cuotas_totales:
                record.estado_de_pago = 'terminado'
    


            
            


class FinancialManagement(models.Model):
    _name = 'financial.management.line'

    financial_id = fields.Many2one(
        'financial.management', string='Lineas de Amortizacion')

    account_id = fields.Many2one('account.move', 'Credito')
    fecha_pago = fields.Datetime()
    fecha_vencimiento_pago = fields.Datetime()
    pagado = fields.Boolean(default=False)
    capital = fields.Integer()
    interes = fields.Integer()  # percentage
    comision_bancaria = fields.Integer()
    valor_cuota = fields.Integer()  # suma de los dos valores anteriores
    saldo_capital = fields.Integer()



class FinancialManagementType(models.Model):
    _name = 'type.credit'

    name = fields.Char(string='Tipo de credito')