# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


import time
from datetime import datetime
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api



class InhSaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    responsible_id = fields.Many2one('res.users', string='Responsable')
    type_sale = fields.Selection([('normal_sale_order', 'Presupuesto Estandar'),('service_sale_order', 'Presupuesto Servicio')], string="Tipo de presupuesto", default="normal_sale_order")
    fleet = fields.Many2one('fleet.vehicle',string='Flota')
    brand = fields.Many2one('fleet.vehicle.model.brand', string='Marca')
    model = fields.Many2one('fleet.vehicle.model', string='Modelo')
    license_plate = fields.Char(string='Patente')
    worker_order_count = fields.Integer(
        compute='_get_worker_order_count', string="worker order")
    
    
    def worker_order_button(self):
        self.ensure_one()

        return {
            'name': 'Sale order OT',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.diagnosys',
            'domain': [('sale_order_id', '=', self.id)],
        }
    
    def _get_worker_order_count(self):
        for sale in self:
            worker_ids = self.env['car.diagnosys'].search(
                [('sale_order_id', '=', sale.id)])
            sale.worker_order_count = len(worker_ids)
    
    def create_worker_order(self):
        
        sale_obj = self.env['sale.order'].browse(self.ids[0])
        
        vals = {
            'name': sale_obj.name,
            'partner_id': sale_obj.partner_id.id,
            'sale_order_id': sale_obj.id,
            'brand': sale_obj.brand.id,
            'model': sale_obj.model.id,
            'license_plate': sale_obj.license_plate,
            'assigned_to': sale_obj.responsible_id.id,
            
            
        }    
        
        car_diagnosys = self.env['car.diagnosys'].create(vals)
        return True
    
