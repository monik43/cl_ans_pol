# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"

    lot_assigned = fields.Boolean("Lote ya asignado", default=False, compute="_compute_in_repair_lines", store=True)
    in_repair_lines = fields.One2many('mrp.repair.line', 'lot_id', "Lineas de operaciones")

    def _compute_in_repair_lines(self):
        for rec in self:
            for line in self.env['mrp.repair.line'].browse([('lot_id','=',rec.id)]):
                rec.update({"in_repair_lines": [(4, line.id)]})
                rec.lot_assigned = True