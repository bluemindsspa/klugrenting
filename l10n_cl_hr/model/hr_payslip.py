from pytz import timezone
from datetime import date, datetime, time

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import pandas as pd

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    indicadores_id = fields.Many2one('hr.indicadores', string='Indicadores',
                                     readonly=True, states={'draft': [('readonly', False)]},
                                     help='Defines Previred Forecast Indicators')
    movimientos_personal = fields.Selection([('0', 'Sin Movimiento en el Mes'),
                                             ('1', 'Contratación a plazo indefinido'),
                                             ('2', 'Retiro'),
                                             ('3', 'Subsidios (L Médicas)'),
                                             ('4', 'Permiso Sin Goce de Sueldos'),
                                             ('5', 'Incorporación en el Lugar de Trabajo'),
                                             ('6', 'Accidentes del Trabajo'),
                                             ('7', 'Contratación a plazo fijo'),
                                             ('8', 'Cambio Contrato plazo fijo a plazo indefinido'),
                                             ('11', 'Otros Movimientos (Ausentismos)'),
                                             ('12', 'Reliquidación, Premio, Bono')
                                             ], 'Código Movimiento', default="0")

    date_start_mp = fields.Date(
        'Fecha Inicio MP',  help="Fecha de inicio del movimiento de personal")
    date_end_mp = fields.Date(
        'Fecha Fin MP',  help="Fecha del fin del movimiento de personal")
    code = fields.Char(string='Codigo', related='indicadores_id.name')



    @api.model
    def _get_worked_day_lines(self, domain=None, check_out_of_contract=True):
        res = super(HrPayslip, self)._get_worked_day_lines(domain, check_out_of_contract)
        # for line in res:
        #     work_entry_type_id = self.env['hr.work.entry.type'].search([('id', '=', line.get('work_entry_type_id'))])
            # lines_worked = []
            # days_eff_per_month = pd.bdate_range(start=str(self.date_from), end=str(self.date_to))
            # dates = [date for date in days_eff_per_month.array.date]
            # if work_entry_type_id.code == 'WORK100':
            #     vals = {
            #         'sequence': line['sequence'],
            #         'work_entry_type_id': work_entry_type_id.id,
            #         'number_of_days': 30,
            #         'number_of_hours': len(dates) * self.contract_id.resource_calendar_id.hours_per_day
            #     }
            # if work_entry_type_id.code == 'EFF100':
            #     vals = {
            #         'sequence': line['sequence'],
            #         'work_entry_type_id': work_entry_type_id.id,
            #         'number_of_days': len(dates),
            #         'number_of_hours': len(dates) * self.contract_id.resource_calendar_id.hours_per_day
            #     }
            # if work_entry_type_id.code == 'LEAVE110':
            #     leaves = self.env['hr.leave'].search([()])
            #     vals = {
            #         'sequence': line['sequence'],
            #         'work_entry_type_id': work_entry_type_id.id,
            #         'number_of_days': len(dates),
            #         'number_of_hours': len(dates) * self.contract_id.resource_calendar_id.hours_per_day
            #     }


        # temp = 0
        # dias = 0
        # attendances = {}
        # leaves = []
        # for line in res:
        #     if line.get('code') == 'WORK100':
        #         attendances = line
        #     else:
        #         leaves.append(line)
        # for leave in leaves:
        #     temp += leave.get('number_of_days') or 0
        # # Dias laborados reales para calcular la semana corrida
        # effective = attendances.copy()
        # effective.update({
        #     'name': _("Dias de trabajo efectivos"),
        #     'sequence': 2,
        #     'code': 'EFF100',
        # })
        # # En el caso de que se trabajen menos de 5 días tomaremos los dias trabajados en los demás casos 30 días - las faltas
        # # Estos casos siempre se podrán modificar manualmente directamente en la nomina.
        # # Originalmente este dato se toma dependiendo de los dias del mes y no de 30 dias
        # # TODO debemos saltar las vacaciones, es decir, las vacaciones no descuentan dias de trabajo.
        # if (effective.get('number_of_days') or 0) < 5:
        #     dias = effective.get('number_of_days')
        # else:
        #     dias = 30 - temp
        # attendances['number_of_days'] = dias
        # res = []
        # res.append(attendances)
        # res.append(effective)
        # res.extend(leaves)
        return res

    def _get_new_worked_days_lines(self):
        HrLeave = self.env['hr.leave']
        HrWorkEntryType = self.env['hr.work.entry.type']
        if self.struct_id.use_worked_day_lines:
            # computation of the salary worked days
            worked_days_line_values = self._get_worked_day_lines()
            work_eff1100 = HrWorkEntryType.search([('code', '=', 'EFF100')])
            days_eff_per_month = pd.bdate_range(start=str(self.date_from), end=str(self.date_to))
            dates = [date for date in days_eff_per_month.array.date]
            worked_days_line_values.append({
                'sequence': work_eff1100.sequence,
                'work_entry_type_id': work_eff1100.id,
                'number_of_days': len(dates),
                'number_of_hours': len(dates) * self.contract_id.resource_calendar_id.hours_per_day
            })
            worked_days_lines = self.worked_days_line_ids.browse([])
            absences = 0
            attendances = []
            leaves = []
            for r in worked_days_line_values:
                r['payslip_id'] = self.id
                worked_days_lines |= worked_days_lines.new(r)
            for work in worked_days_lines:
                if work.code == 'WORK100':
                    work.number_of_days = 30
                    attendances.append(work)
                elif work.code == 'EFF100':
                    attendances.append(work)
                else:
                    leave = HrLeave.search([
                        ('employee_id', '=', work.payslip_id.employee_id.id),
                        ('date_from', '>=', work.payslip_id.date_from),
                        ('date_from', '<=', work.payslip_id.date_to),
                        ('date_to', '>=', work.payslip_id.date_from),
                        ('date_to', '<=', work.payslip_id.date_to)])
                    for l in leave:
                        absences += l.number_of_days
                    work.number_of_days = absences
                    leaves.append(work)
            if attendances:
                for attendance in attendances:
                    if absences > 0 and attendance.work_entry_type_id.code == 'WORK100':
                        attendance.update({
                            'number_of_days': attendance.number_of_days - absences if attendance.number_of_days > absences else 0
                        })
                    # else:
                    #     attendance.update({
                    #         'number_of_days': 30
                    #     })
            return worked_days_lines
        else:
            return [(5, False, False)]
