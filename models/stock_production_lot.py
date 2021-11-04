# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"

    lot_assigned = fields.Boolean("Lote ya asignado", default=False, compute="_compute_lot_assigned")

    def _compute_lot_assigned(self):
        for rec in self:
            if self.env['mrp.repair.line'].search([('lot_id','=',rec.lot_id.id),('lot_id','!=', '9999')]):
                print("El nº de lote ya está asignado en otra reparación. ", "/"*50)
                rec.lot_assigned = True