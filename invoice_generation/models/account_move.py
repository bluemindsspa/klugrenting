# -*- coding: utf-8 -*-

import random
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    scheduled_date = fields.Date('Fecha Pautada')
    mass_invoice = fields.Boolean('Factura Masiva')
    uf_rate = fields.Float('Tasa UF', default=lambda self: self._get_uf())

    def _get_uf(self):
        uf = self.env['res.currency'].search([('name', '=', 'UF')])
        rate = 0.0
        if uf:
            rate = 1 / uf.rate if uf.rate else 0.0
        return rate

    @api.onchange('uf_rate')
    def set_uf_rate(self):
        self.invoice_line_ids.set_uf_rate()
        self.line_ids.my_balance()

    def cron_invoice_public(self):
        # search for invoices of the day to be published
        print("***_cron_invoice_public***")
        today_date = fields.Datetime.now()
        invoices = self.env['account.move'].search([('scheduled_date', '=', today_date),
                                                    ('type', '=', 'out_invoice'),
                                                    ('mass_invoice', '=', True)])
        if invoices:
            for inv in invoices:
                inv.action_post()
        return True

    # @api.constrains("reference", "partner_id", "company_id", "move_type", "journal_document_class_id")
    @api.constrains("reference", "partner_id", "company_id", "move_type", "l10n_latam_document_type_id")
    def _check_reference_in_invoice(self):
        for record in self:
            # if record.move_type in ["in_invoice", "in_refund"] and record.sii_document_number:
            if record.move_type in ["in_invoice", "in_refund"] and record.l10n_latam_document_number:
                domain = [
                    ("move_type", "=", record.move_type),
                    # ("sii_document_number", "=", record.sii_document_number),
                    ("l10n_latam_document_number", "=", record.l10n_latam_document_number),
                    ("partner_id", "=", record.partner_id.id),
                    # ("journal_document_class_id.sii_document_class_id", "=", record.journal_document_class_id.id),
                    ("l10n_latam_document_type_id", "=", record.l10n_latam_document_type_id.id),
                    ("company_id", "=", record.company_id.id),
                    ("id", "!=", record.id),
                    ("state", "!=", "cancel"),
                ]
                move_ids = record.search(domain)
                if move_ids:
                    raise UserError(
                        u"El numero de factura debe ser unico por Proveedor.\n"
                        u"Ya existe otro documento con el numero: %s para el proveedor: %s"
                        % (record.l10n_latam_document_number, record.partner_id.display_name)
                    )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    uf_rate = fields.Float(related='move_id.uf_rate', string='Tasa UF')
    set_uf = fields.Float(string='Setear Tasa UF')

    def set_uf_rate(self):
        sale_order_id = self.env['sale.order'].search([('name', '=', self.move_id.invoice_origin)])
        for ol in sale_order_id.order_line:
            for il in self:
                if ol.product_id == il.product_id:
                    price_unit = ol.price_unit * il.uf_rate
                    il.write({'price_unit': price_unit})

    def my_balance(self):
        credit = sum(l.credit for l in self)
        for bl in self:
            if bl.credit == 0:
                bl.write({'debit': credit})
