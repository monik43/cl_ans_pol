# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class helpdesk_stage(models.Model):
    _inherit = "helpdesk.stage"

    sla_id = fields.Many2one('helpdesk.sla', 'Politica ANS')


class helpdesk_ticket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange('stage_id')
    def onchange_stage_id_eq_sla_id(self):
        for ticket in self:
            if not ticket.stage_id.sla_id and self.env['helpdesk.sla'].search([('name', '=', ticket.stage_id.name)]):
                ticket.sla_id = self.env['helpdesk.sla'].search([('name', '=', ticket.stage_id.name)])
            elif ticket.stage_id.sla_id:
                ticket.sla_id = ticket.stage_id.sla_id
