# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from datetime import date
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


class SaleOrder(models.Model):
    _inherit = "sale.order"

    #scheduled_date = fields.Date('Fecha Pautada')
    scheduled_date = fields.Date('Fecha Pautada', default=fields.Date.today())
    mass_invoice = fields.Boolean('Factura Masiva')
    uf_rate = fields.Float('Tasa UF')

    def _prepare_invoice(self):
        today = date.today()
        res = super(SaleOrder, self)._prepare_invoice()
        if self.currency_id.name == 'UF':
            uf_rate = self.currency_id.rate or 1
            clp = self.env['res.currency'].search([('name', '=', 'CLP')])
            res['currency_id'] = clp.id
        res['scheduled_date'] = self.scheduled_date
        res['invoice_date'] = self.scheduled_date
        res['mass_invoice'] = self.mass_invoice
        res['uf_rate'] = 1 / uf_rate
        #res['reference_ids'] = self.reference_ids
        # if self.reference_ids.date_init <= today and self.reference_ids.date_end >= today:
        #     raise UserError(_('La referencia esta vencida'))
        return res

    def _get_invoice_grouping_keys(self):
        return ['company_id', 'partner_id']


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if self.currency_id.name == 'UF':
            # try:
            if self.currency_id.rate > 0:
                rate = 1 / self.currency_id.rate
                res['price_unit'] = res['price_unit'] * rate
            # except ZeroDivisionError:
            #     res['price_unit'] = 0
        return res

    # def _get_uf(self):
    #     uf = self.env['res.currency'].search([('name', '=', 'UF')])
    #     rate = 1 / float(uf.rate)
    #     return rate