# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class mrp_repair(models.Model):
    _inherit="mrp.repair"
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('product_id','=', product_id)]",
        help="Products repaired are all belonging to this lot", oldname="prodlot_id", store=True)