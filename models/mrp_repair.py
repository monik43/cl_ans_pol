# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'

    @api.onchange('location_id')
    def onchange_location_id(self):
        self.location_dest_id = self.location_id.id

        for line in self.operations:
            line.location_id = self.location_id