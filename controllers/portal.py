# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request, route
from odoo.tools import consteq
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomCustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        user_is_company = True

        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        if request.env["res.users"].browse(request.uid).partner_id.company_type == "person":
            user_is_company = False

        print(f" _prepare_portal_layout_values ---- {user_is_company}", "/" * 50)
        return {
            "user_is_company": user_is_company,
            "sales_user": sales_user,
            "page_name": "home",
            "archive_groups": [],
        }

    @route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        print(values)
        return request.render("portal.portal_my_home", values)
