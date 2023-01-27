# © 2022 (Daniel Fernandez <daniel@klugrenting.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _
import datetime
import ast
import json


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    
    def create_account(self):
        # call picking function
        
        #self.consume_car_parts()
        list_invoice = []
        res = {}
        values = {}
        values_product = {}
        sale_order_obj = self.env['sale.order'].browse(self.ids[0])
       
        journal_id = self.env['account.journal'].search([('type', '=', 'sale'), (
            'name', '=', 'Facturas de cliente'), ('company_id', '=', self.company_id.id)])
        type_document = self.env['l10n_latam.document.type'].search(
            [('code', '=', 33)])
        currency = self.env['res.currency'].search([('name', '=', 'CLP')])
        taxes = self.env['account.tax'].search([('type_tax_use', '=', 'sale')])
        tax_ids = [tax.id for tax in taxes if tax.l10n_cl_sii_code ==
                   14 and tax.description == 'IVA 19% Venta']
        invoice = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'currency_id': currency.id,
            'state': 'draft',
            'invoice_date': datetime.datetime.now(),
            'journal_id': journal_id.id,
            'l10n_latam_document_type_id': type_document.id,


        })

        for line in sale_order_obj.order_line:
            values = {
                'move_id': invoice.id,
                'name': line.name,
                'product_id': 746 if line.product_id.categ_id.name == 'Vehículo' else line.product_id.id,
                # 'account_id': journal_id.default_account_id.id,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
                'tax_ids': line.product_id.taxes_id.ids,
            }

            list_invoice.append(values)
        

        invoice.write(
            {'invoice_line_ids': [(0, 0, values) for values in list_invoice]})
        invoice._onchange_partner_id()
        invoice._onchange_invoice_line_ids()
        invoice._move_autocomplete_invoice_lines_values()