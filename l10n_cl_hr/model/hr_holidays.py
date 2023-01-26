
import math
import pandas as pd
from odoo import api, fields, models, tools


class HRHolidaysStatus(models.Model):
    _inherit = 'hr.leave.type'
    is_continued = fields.Boolean('Disccount Weekends')


class HRHolidays(models.Model):
    _inherit = 'hr.leave'

    def _get_number_of_days(self, date_from, date_to, employee_id):
        #En el caso de las licencias descontamos dias corridos
        if employee_id and self.holiday_status_id.is_continued:
            time_delta = pd.date_range(self.date_from, self.date_to, tz='America/Santiago')
            hours = self.env.company.resource_calendar_id.get_work_hours_count(date_from, date_to)
            dates = [date for date in time_delta.array.date]
            days = len(dates)
            self.number_of_days = len(dates)
            return {'days': days, 'hours': hours}
        else:
            return super(HRHolidays, self)._get_number_of_days(date_from, date_to, employee_id)


# def _get_number_of_days(self, date_from, date_to, employee_id):
#   186          """ If an employee is currently working full time but requests a leave next month
#   187              where he has a new contract working only 3 days/week. This should be taken into
#   ...
#   190              at the time of the leave.
#   191          """
#   192:         days = super(HrLeave, self)._get_number_of_days(date_from, date_to, employee_id)
#   193          if employee_id:
#   194              employee = self.env['hr.employee'].browse(employee_id)

    # @api.depends('date_from', 'date_to', 'employee_id')
    # def _compute_number_of_days(self):
    #     for holiday in self:
    #         if holiday.date_from and holiday.date_to and holiday.employee_id:
    #             time_delta = pd.date_range(
    #                 holiday.date_from, holiday.date_to, tz='America/Santiago')
    #             dates = [date for date in time_delta.array.date]
    #             holiday.number_of_days = len(dates)
    #         else:
    #             holiday.number_of_days = 0
