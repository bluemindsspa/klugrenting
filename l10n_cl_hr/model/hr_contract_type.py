from odoo import api, fields, models, tools, _


class hr_contract_type(models.Model):
    _name = 'hr.contract.type'
    _description = 'Tipo de Contrato'

    name = fields.Char('Nombre')
    codigo = fields.Char('Codigo')