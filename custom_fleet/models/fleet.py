# © 2022 (Jamie Escalante <jescalante@blueminds.cl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _


class InheritFleet(models.Model):
    _inherit = 'fleet.vehicle'
    
    date_delivery = fields.Date(string="Fecha entrega de Vehiculo", related='subscription.date_start')
    date_return = fields.Date(string="Fecha devolucion de Vehiculo", related='subscription.date')
    subscription = fields.Many2one('sale.subscription',string='subscripcion activa')
    traccion_vehicle = fields.Selection([('4x4', '4x4'),('4x2', '4x2'),('AWD', 'AWD')])
    accesories_vehicle = fields.Many2many('accesories.tags', string='Accesorios de Vehiculo', store=True)
    purchase = fields.Many2one('purchase.order', string="Orden de compra")
    date_purchase = fields.Datetime(string="Fecha de Compra")
    account_move = fields.Many2one('account.move', string="Factura OC")
    date_account = fields.Datetime(string="Fecha de Factura")

    
    # @api.depends()
    # def _compute_account(self):
    #     if self.product_id:
    #         account_move_id = self.env['account.move.line'].search([('product_id', '=', self.product_id.id)]) 
    #         if account_move_id:
    #             for record in account_move_id:
    #                 if record.move_id.move_type == 'in_invoice':
    #                     self.account_move = record.move_id.id
    #                     if self.account_move:
    #                         self.date_account = self.account_move.invoice_date
     #
    def _get_odometer(self):
        FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
        for record in self:
            vehicle_odometer = FleetVehicalOdometer.search([('vehicle_id', '=', record.id), ('tag_ids', 'in', [2])], order='id desc',limit=1)
            if vehicle_odometer:
                record.odometer = vehicle_odometer.value
            else:
                record.odometer = 0


    @api.onchange('product_id')
    def _onchange_purchase(self):
        if self.product_id:
            purchase_partner_id = self.env['purchase.order.line'].search([('product_id', '=', self.product_id.id)])
            if purchase_partner_id:
                    self.purchase = purchase_partner_id.order_id.id
                    if self.purchase:
                        self.date_purchase = self.purchase.date_approve
    

    # @api.depends()
    # def _compute_subscription(self):
    #     for record in self:
    #         subscription_ids = self.env['sale.subscription'].search([('vehicle_id','=', record.id)])
    #         if subscription_ids:
    #             record.subscription = subscription_ids.id



class InheritFleetAssignation(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'
    
    date_delivery = fields.Date(string="Fecha entrega de Vehiculo",related='vehicle_id.date_delivery')
    date_return = fields.Date(string="Fecha devolucion de Vehiculo", related='vehicle_id.date_return')
    


class AccesoriesTags(models.Model):

    _name = 'accesories.tags'


    name = fields.Char(string="Nombre")
    color = fields.Integer(string="Color")
