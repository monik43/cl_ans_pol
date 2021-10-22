# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request, route
from odoo.tools import consteq
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomCustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomCustomerPortal, self)._prepare_portal_layout_values()
        user_is_company = True
        if request.env["res.users"].browse(request.uid).partner_id.company_type == "person":
            user_is_company = False
        values['user_is_company'] = user_is_company
        print(values)
        return values
