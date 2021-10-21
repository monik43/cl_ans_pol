# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomCustomerPortal(CustomerPortal):
    @route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        res = super(CustomCustomerPortal, self).home(**kw)
        user_is_company = True
        if (
            request.env["res.users"].browse(request.uid).partner_id.company_type
            == "person"
        ):
            user_is_company = False
        print(f" _prepare_portal_layout_values ---- {user_is_company}", "/" * 50)
        return res
