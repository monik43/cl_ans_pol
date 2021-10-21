# -*- coding: utf-8 -*-

import math

from werkzeug import urls

from odoo import fields as odoo_fields, tools, _
from odoo.osv import expression
from odoo.exceptions import ValidationError
from odoo.http import Controller, request, route
from odoo.addons.web.controllers.main import WebClient
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomCustomerPortal(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        user_is_company = True

        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        if (
            request.env["res.users"].browse(request.uid).partner_id.company_type
            == "person"
        ):
            user_is_company = False

        return {
            "sales_user": sales_user,
            "page_name": "home",
            "archive_groups": [],
            "user_is_company": user_is_company,
        }
