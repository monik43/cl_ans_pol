# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class mrp_repair_line(models.Model):
    _inherit = "mrp.repair.line"

    lot_assigned = fields.Boolean("Lote ya asignado", default=False, compute="_compute_lot_assigned")

    def _compute_lot_assigned(self):
        for rep in self:
            if self.env['mrp.repair.line'].search([('lot_id','=',rep.lot_id)]):
                print("El nº de lote ya está asignado en otra reparación. ", "/"*50)
                rep.lot_assigned = True