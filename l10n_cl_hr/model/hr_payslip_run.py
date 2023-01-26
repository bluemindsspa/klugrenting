from odoo import api, fields, models, tools, _

from datetime import datetime

class hr_payslip_run(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Run'

    indicadores_id = fields.Many2one('hr.indicadores', 'Indicadores', states={'draft': [('readonly', False)]}, readonly=True, required=True)
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
    ], 'Movimientos Personal', default="0")

    def _default_indicador(self):
        class_indicadores = self.env['hr.indicadores']
        periodo = self.date_from  # Obtiene fecha y hora actual
        print("Mes:",periodo.month)  # Muestra mes
        #print("Mes:",ahora.date("%m"))  # Muestra mes
        print("Año:",periodo.year)  # Muestra año
        indicador_mes = class_indicadores.search([ ("month" ,'=', str(periodo.month)) ,  ("year" ,'=', str(periodo.year)) ])
        print( len(indicador_mes))
        if len(indicador_mes) != 0:
            indicador.get_name()
        else:
            #reset your fields 
            #self.your_field1= False
            res['warning'] = {'title': _('Warning'), 'message': _('Revise los indicadores del mes')}
            return res
