# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"

    lot_assigned = fields.Boolean("Lote ya asignado", default=False, compute="_compute_lot_assigned")

    def _compute_lot_assigned(self):
        for rec in self:
            if self.env['mrp.repair.line'].search([('lot_id.id','=',rec.id),('lot_id','!=', '9999')]):
                rec.lot_assigned = True