# -*- coding: utf-8 -*-

import math

from werkzeug import urls
from odoo import http
from odoo import fields as odoo_fields, tools, _
from odoo.osv import expression
from odoo.exceptions import ValidationError
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomCustomerPortal(CustomerPortal):
    @route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        res = super(CustomCustomerPortal, self).home()
        user_is_company = True
        if (
            request.env["res.users"].browse(request.uid).partner_id.company_type
            == "person"
        ):
            user_is_company = False
        print(f" _prepare_portal_layout_values --- {user_is_company}", "/" * 50)
        return res
