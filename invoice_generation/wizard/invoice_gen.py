# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError
from logging import getLogger

_logger = getLogger(__name__)


class InvoiceGen(models.TransientModel):
    _name = 'invoice.gen'
    _description = u'Generación de Facturas'

    date_from = fields.Date('Fecha desde')
    date_to = fields.Date('Fecha hasta')
    type_gen = fields.Selection(selection=[
        ('u', 'Generar facturas unidas'),
        ('d', 'Generar facturas divididas')
    ], string='Tipo de Generación', required=True)
    partner_id = fields.Many2one('res.partner', 'Cliente', domain=[])
    uf_rate = fields.Float('Tasa UF', digits=(16, 2), default=lambda self: self._get_uf())
    scheduled_date = fields.Date('Fecha Pautada')

    def _get_uf(self):
        uf = self.env['res.currency'].search([('name', '=', 'UF')])
        if uf:
            rate = (1 / uf.rate) if uf.rate else 0.0
        return rate

    def generate_invoices(self):
        s_default = [
            ('state', '=', 'sale'),
            ('scheduled_date', '>=', self.date_from),
            #('fecha_fact_prog', '>=', self.date_from),
            ('scheduled_date', '<=', self.date_to),
            #('fecha_fact_prog', '<=', self.date_to),
            ('invoice_status', '=', 'to invoice')
        ]
        if self.partner_id:
            s_default.append(('partner_id', '=', self.partner_id.id))
        # agreements = []
        # order_ids = self.env['sale.order'].search(s_default, order='partner_id')
        # for validacion in order_ids:
        #     if validacion.agreement_line_ids.state != 'act':
        #         agreements.append(validacion.agreement_id.id)
        #     if validacion.agreement_id.req_orden:
        #         if validacion.agreement_id.reference_ids:
        #             for reference in validacion.agreement_id.reference_ids:
        #                 codes = []
        #                 if validacion.agreement_id.l10ncl_domain:
        #                     for cod in validacion.agreement_id.l10ncl_domain:
        #                         codes.append(cod.code)
        #                 if reference.l10n_cl_reference_doc_type_selection not in codes:
        #                     agreements.append(validacion.agreement_id.id)
        #                 if reference.date_init >= date.today():
        #                     agreements.append(validacion.agreement_id.id)
        #                 if reference.date_end <= date.today():
        #                     agreements.append(validacion.agreement_id.id)
        #         else:
        #             agreements.append(validacion.agreement_id)
        # if agreements:
        #     s_default.append(('agreement_id', 'not in', list(set(agreements))))
        order_ids = self.env['sale.order'].search(s_default, order='partner_id')
        for line in order_ids:
                vals = {
                    'scheduled_date': self.scheduled_date,
                    'mass_invoice': True,
                    'uf_rate': self.uf_rate
                }
                line.write(vals)

        if order_ids:
            if self.type_gen == 'u':
                inv_id = order_ids._create_invoices()
            else:
                inv_id = order_ids._create_invoices(grouped=True)
        else:
            raise ValidationError('No se encontraron registros coincidentes')
            # pass
