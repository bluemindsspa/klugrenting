# -*- coding: utf-8 -*-
##############################################################################
# Chilean Payroll
# Odoo / OpenERP, Open Source Management Solution
# Copyright (c) 2015 Blanco Martin y Asociados
# Nelson Ramírez Sánchez - Daniel Blanco
# http://blancomartin.cl
#
# Derivative from Odoo / OpenERP / Tiny SPRL
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields

# from datetime import date, datetime, timedelta



class hr_contract2(models.Model):

    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    hr_discount = fields.Float('Horas a descontar', help="Horas a descontar")
    cumplimiento_meta = fields.Float(
        'Bono Cumplimiento meta', help="Bono cumplimiento")
    evaluacion_desemp = fields.Float(
        'Bono Atencion Cliente',
        help="Bono Atencion Cliente")
    comisiones = fields.Float(
        'Comisiones',
        help="Comisiones")
    horas_extras = fields.Float(
        'Horas Extras 50%',
        help="Horas_extras")
    retencion_judicial = fields.Float(
        'Descuento Retención Judicial',
        help="Descuento Retención Judicial")            
    prestamo = fields.Float('Horas extras 100%', help="Horas extras")

    variante1 = fields.Float('Dias presencia')
    variante2 = fields.Float('Bono Extra')
    variante3 = fields.Float('Bono Nocturno')
    variante4 = fields.Float('Bono de Produccion')
    variante5 = fields.Float('Convenio Falp')
    variante6 = fields.Float('Bono de Incentivo')            
    variante7 = fields.Float('Aguinaldo')
    variante8 = fields.Float('Descuento Acid SA')
    variante9 = fields.Float('Descuento Casino')
    variante10 = fields.Float('Descuento Chilena')
    variante11 = fields.Float('Cuota sindicato')
    variante12 = fields.Float('Descuento Dental')

    antiguedad = fields.Integer(
        string='Antiguedad',
        readonly=True,
        compute='_compute_antiq',
    )

    #@api.multi
    @api.depends('date_start')
    def _compute_antiq(self):
        for record in self:
            antiguedad = 0
            if record.date_start:
                antiguedad = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.date_start)).years
            record.antiguedad = antiguedad


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    age = fields.Integer(
        string='Age',
        readonly=True,
        compute='_compute_age',
    )

    #@api.multi
    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthday:
                age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.birthday)).years
            record.age = age



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
