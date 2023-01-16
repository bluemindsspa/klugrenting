# -*- coding: utf-8 -*-
import base64
import io
import datetime
import werkzeug
from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, MissingError
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools.translate import _
from collections import Counter
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import get_records_pager, pager as portal_pager





class CustomerPortal(portal.CustomerPortal):
    
    
    @http.route(['/my/subscription/<int:subscription_id>/download/1', ], type='http', auth='public')
    def download_attachmentt(self, subscription_id,  access_token=None, **kw):
        # Check if this is a valid attachment id

        try:
            subscription_sudo = self._document_check_access(
                'sale.subscription', subscription_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._prepare_portal_layout_values()
        if subscription_sudo.attach_1:
            data = io.BytesIO(base64.standard_b64decode(subscription_sudo.attach_1))
            return http.send_file(data, filename=subscription_sudo.attach_1_fname, as_attachment=True)
        

        else:
            return request.not_found()

    @http.route(['/my/subscription/<int:subscription_id>/download/2', ], type='http', auth='public')
    def download_attachmentt2(self,subscription_id,  access_token=None, **kw):
        # Check if this is a valid attachment id
        

        try:
            subscription_sudo = self._document_check_access(
                'sale.subscription', subscription_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._prepare_portal_layout_values()
        if subscription_sudo.attach_2:
            data2=io.BytesIO(base64.standard_b64decode(subscription_sudo.attach_2))
            return http.send_file(data2, filename =subscription_sudo.attach_2_fname, as_attachment = True)
            
        else:
            return request.not_found()
        
    @http.route(['/my/subscription/<int:subscription_id>/download/3', ], type='http', auth='public')
    def download_attachmentt3(self,subscription_id,  access_token=None, **kw):
        # Check if this is a valid attachment id
        

        try:
            subscription_sudo = self._document_check_access(
                'sale.subscription', subscription_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._prepare_portal_layout_values()
        if subscription_sudo.attach_3:
            data3=io.BytesIO(base64.standard_b64decode(subscription_sudo.attach_3))
            return http.send_file(data3, filename =subscription_sudo.attach_3_fname, as_attachment = True)
            
        else:
            return request.not_found()
        
        
    @http.route(['/my/subscription/<int:subscription_id>/download/4', ], type='http', auth='public')
    def download_attachmentt4(self,subscription_id,  access_token=None, **kw):
        # Check if this is a valid attachment id
        

        try:
            subscription_sudo = self._document_check_access(
                'sale.subscription', subscription_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._prepare_portal_layout_values()
        if subscription_sudo.attach_4:
            data4=io.BytesIO(base64.standard_b64decode(subscription_sudo.attach_4))
            return http.send_file(data4, filename =subscription_sudo.attach_4_fname, as_attachment = True)
            
        else:
            return request.not_found()
        
        
    @http.route(['/my/subscription/<int:subscription_id>/download/5', ], type='http', auth='public')
    def download_attachmentt5(self,subscription_id,  access_token=None, **kw):
        # Check if this is a valid attachment id
        

        try:
            subscription_sudo = self._document_check_access(
                'sale.subscription', subscription_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._prepare_portal_layout_values()
        if subscription_sudo.attach_5:
            data5=io.BytesIO(base64.standard_b64decode(subscription_sudo.attach_5))
            return http.send_file(data5, filename =subscription_sudo.attach_5_fname, as_attachment = True)
            
        else:
            return request.not_found()
        
        
    @http.route(['/my/subscription/<int:subscription_id>/download/6', ], type='http', auth='public')
    def download_attachmentt6(self,subscription_id,  access_token=None, **kw):
        # Check if this is a valid attachment id
        

        try:
            subscription_sudo = self._document_check_access(
                'sale.subscription', subscription_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._prepare_portal_layout_values()
        if subscription_sudo.attach_6:
            data6=io.BytesIO(base64.standard_b64decode(subscription_sudo.attach_6))
            return http.send_file(data6, filename =subscription_sudo.attach_6_fname, as_attachment = True)
            
        else:
            return request.not_found()