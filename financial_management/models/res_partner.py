# © 2022 (Daniel Fernandez <daniel@klugrenting.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _

import ast
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    comision_credito = fields.Integer(default=0)
    monto_seguro = fields.Integer(default=0)
    entidad_bancaria = fields.Many2one(comodel_name='res.partner', string='Entidad Bancaria')


