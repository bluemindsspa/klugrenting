# © 2022 (Jamie Escalante <jescalante@blueminds.cl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _
import base64
import logging
from io import BytesIO
from xlwt import Workbook, easyxf
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import time
from datetime import timedelta, datetime
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'
    
    
    
    
    deducible_maliciosos = fields.Integer('deducible malicioso')
    deducible_robo = fields.Integer('deducible robo')
    deducible_propios_terceros = fields.Integer('Danos propios y a Terceros')
    deducible_accesorios = fields.Integer('Robo accesorios')
    fecha_contrato = fields.Date('Fecha Contrato')
    maintenance = fields.Char(string="Frecuencia de mantenimiento")
    pago_garantia = fields.Boolean(default=False) 
    
