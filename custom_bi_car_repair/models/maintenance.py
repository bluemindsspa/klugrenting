# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, SUPERUSER_ID, _, tools


class InhAccountMove(models.Model):
    _inherit = 'account.move'

    maintenance_id = fields.Many2one('maintenance.request', string='OT')


class InhMaintenance(models.Model):
    _inherit = 'maintenance.request'

    partner_id = fields.Many2one('res.partner', string='Cliente')
    fleet = fields.Many2one('fleet.vehicle', string='Flota')
    brand = fields.Many2one('fleet.vehicle.model.brand', string='Marca')
    model = fields.Many2one('fleet.vehicle.model', string='Modelo')
    license_plate = fields.Char(string='Patente')
    year = fields.Char(string='Año')
    color = fields.Char(string='Color')
    sale_order_id = fields.Many2one('sale.order', string='Origen')
    failure = fields.Char(string='Falla')
    state_vehicule = fields.Char(string='Estado vehiculo')
    image_brand = fields.Binary(
        string="imagen marca", compute='_compute_image_vals')
    image_one = fields.Binary(string="imagen 1")
    image_two = fields.Binary(string="imagen 2")
    image_tree = fields.Binary(string="imagen 3")
    image_four = fields.Binary(string="imagen 4")
    image_five = fields.Binary(string="imagen 5")
    maintenance_line_products = fields.One2many(
        'maintenance.line.products', 'sale_order_product_id')
    maintenance_line_services = fields.One2many(
        'maintenance.line.services', 'sale_order_service_id')
    observations = fields.Text(string='Observaciones')
    odometer = fields.Integer(string='Odometro')
    account_count = fields.Integer(
        compute='_get_account_count', string="Factura")
    picking_count = fields.Integer(
        compute='_get_picking_count', string="Factura")

    def account_move_button(self):
        self.ensure_one()

        return {
            'name': 'OT order invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('maintenance_id', '=', self.id)],
        }

    def _get_account_count(self):
        for account in self:
            account_ids = self.env['account.move'].search(
                [('maintenance_id', '=', account.id)])
            account.account_count = len(account_ids)

    @api.depends('image_brand')
    def _compute_image_vals(self):
        self.image_brand = self.brand.image_128

    def _get_picking_count(self):
        for picking in self:
            picking_ids = self.env['stock.picking'].search(
                [('origin', '=', self.name)])
            picking.picking_count = len(picking_ids)

    def picking_button(self):
        self.ensure_one()
        return {
            'name': 'Consume Parts Picking',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.name)],
        }

    def consume_car_parts(self):

        picking_type_id = self.env['stock.picking.type'].search([['code', '=', 'outgoing'], [
                                                                'warehouse_id.company_id', '=', self.company_id.id]], limit=1)

        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type_id.id,
            'picking_type_code': 'outgoing',
            'location_id': picking_type_id.default_location_src_id.id,
            'location_dest_id': picking_type_id.default_location_dest_id.id,
            'origin': self.name,
        })
        for estitmate in self.maintenance_line_products:
            move = self.env['stock.move'].create({
                'picking_id': picking.id,
                'name': estitmate.product_id.name,
                'product_uom': estitmate.product_id.uom_id.id,
                'product_id': estitmate.product_id.id,
                'product_uom_qty': estitmate.quantity,
                'location_id': picking_type_id.default_location_src_id.id,
                'location_dest_id': picking_type_id.default_location_dest_id.id,
                'origin': self.name,
            })

    def create_account(self):
        list_invoice = []
        res = {}
        values = {}
        maintenance_obj = self.env['maintenance.request'].browse(self.ids[0])
        car_repair_obj = self.env['car.repair']
        product_obj = self.env['product.product']

        journal_id = self.env['account.journal'].search([('type', '=', 'sale'), (
            'name', '=', 'Facturas de cliente'), ('company_id', '=', self.company_id.id)])
        type_document = self.env['l10n_latam.document.type'].search(
            [('code', '=', 33)])
        currency = self.env['res.currency'].search([('name', '=', 'CLP')])
        taxes = self.env['account.tax'].search([('type_tax_use', '=', 'sale')])
        tax_ids = [tax.id for tax in taxes if tax.l10n_cl_sii_code ==
                   14 and tax.description == 'IVA 19% Venta']
        invoice = self.env['account.move'].create({
            'partner_id': maintenance_obj.partner_id.id,
            'move_type': 'out_invoice',
            'currency_id': currency.id,
            'state': 'draft',
            'invoice_date': datetime.now(),
            'journal_id': journal_id.id,
            'maintenance_id': maintenance_obj.id,
            'l10n_latam_document_type_id': type_document.id,


        })

        for services_line in maintenance_obj.maintenance_line_services:
            values['move_id'] = invoice.id
            values['name'] = services_line.description,
            values['product_id'] = services_line.product_id.id
            values['account_id'] = journal_id.default_account_id.id
            values['quantity'] = services_line.quantity
            values['price_unit'] = services_line.price
            values['account_id'] = services_line.product_id.categ_id.property_account_income_categ_id.id,
            values['tax_ids'] = services_line.product_id.taxes_id.ids

            list_invoice.append(values)
        for products_line in maintenance_obj.maintenance_line_products:
            values['move_id'] = invoice.id
            values['name'] = products_line.description,
            values['product_id'] = products_line.product_id.id
            values['account_id'] = journal_id.default_account_id.id
            values['quantity'] = products_line.quantity
            values['price_unit'] = products_line.price
            values['account_id'] = products_line.product_id.categ_id.property_account_income_categ_id.id,
            values['tax_ids'] = products_line.product_id.taxes_id.ids

            list_invoice.append(values)

        invoice.write(
            {'invoice_line_ids': [(0, 0, values) for values in list_invoice]})
        invoice._onchange_partner_id()
        invoice._onchange_invoice_line_ids()
        invoice._move_autocomplete_invoice_lines_values()

    # @api.onchange('maintenance_line_services')
    # def onchange_maintenance_line_services(self):
    #     for record in self.maintenance_line_services:
    #         record.total_price += record.price
    #         record.total_quantity += record.quantity


class InhMaintenanceLineProducts(models.Model):

    _name = 'maintenance.line.products'

    product_id = fields.Many2one('product.product', string='Productos')
    description = fields.Char(string='Descripción')
    price = fields.Float(string='Precio')
    quantity = fields.Float(string='Cantidad')
    sale_order_product_id = fields.Many2one('sale.order', string='Presupuesto')
    total_price = fields.Float(string='Precio total')
    total_quantity = fields.Float(string='Cantidad total')


class InhMaintenanceLineServices(models.Model):

    _name = 'maintenance.line.services'

    product_id = fields.Many2one('product.product', string='Productos')
    description = fields.Char(string='Descripción')
    price = fields.Float(string='Precio')
    quantity = fields.Float(string='Cantidad')
    sale_order_service_id = fields.Many2one('sale.order', string='Presupuesto')
    total_price = fields.Float(string='Precio total')
    total_quantity = fields.Float(string='Cantidad total')
