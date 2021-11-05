# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"

    #lot_assigned = fields.Boolean("Lote ya asignado", default=False, compute="_compute_lot_assigned", store=True)
    in_repair_lines = fields.One2many('mrp.repair.line', 'lot_id', "Lineas de operaciones")

    def _compute_in_repair_lines(self):
        for rec in self:
            for line in self.env['mrp.repair.line'].browse([('lot_id','=',rec.id)]):
                rec.update({"in_repair_lines": [(4, line.id)]})

    """@api.depends("product_id")
    def _compute_lot_assigned(self):
        for rec in self:
            print(rec.product_id, " ", rec.name, " ", "//"*25)
            if rec.product_id and self.env['mrp.repair.line'].search([('lot_id.id','=',rec.id)]):
                #rec.lot_assigned = True
                print(rec.lot_assigned, rec.product_id, "/"*50)"""