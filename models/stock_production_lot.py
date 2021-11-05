# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"

    lot_assigned = fields.Boolean("Lote ya asignado", default=False, compute="_compute_lot_assigned", store=True)

    @api.depends("product_id")
    def _compute_lot_assigned(self):
        for rec in self:
            if rec.product_id and rec.name != '9999' and self.env['mrp.repair.line'].search([('lot_id.id','=',rec.id)]):
                rec.lot_assigned = True
                print(rec.lot_assigned, rec.product_id)