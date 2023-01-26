from odoo import api, fields, models, tools, _


class hr_termination_reason_contract(models.Model):
    _name = 'hr.termination.reason.contract'
    _description = 'Razón de finalización del contrato'
    codigo = fields.Char(string='Code')
    name = fields.Char(string='Name')