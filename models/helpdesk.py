# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class helpdesk_stage(models.Model):
    _inherit = "helpdesk.stage"

    sla_id = fields.Many2one('helpdesk.sla', 'Politica ANS')
    def_assign = fields.Many2one('res.users', 'Técnico')


class helpdesk_ticket(models.Model):
    _inherit = "helpdesk.ticket"

    def _get_historial_tickets(self):
        for ticket in self:
            for t in self.env['helpdesk.ticket'].search(['|', ('x_sn', '=', ticket.x_sn), ('x_lot_id', '=', ticket.x_lot_id)]):
                print(f"{t.name} -- {t.id}, {t.stage_id.name} #")

    @api.onchange('stage_id')
    def onchange_stage_id_eq_sla_id(self):
        for ticket in self:
            # asignacion politica ans correcta
            if not ticket.stage_id.sla_id and self.env['helpdesk.sla'].search([('name', '=', ticket.stage_id.name)]):
                ticket.sla_id = self.env['helpdesk.sla'].search(
                    [('name', '=', ticket.stage_id.name)])
            elif ticket.stage_id.sla_id:
                ticket.sla_id = ticket.stage_id.sla_id
            # asignacion usuario x defecto
            if ticket.stage_id.def_assign and ticket.user_id != ticket.stage_id.def_assign:
                print(
                    f"default: {ticket.stage_id.def_assign} _ user_id: {ticket.user_id}")
                ticket.user_id = ticket.stage_id.def_assign

    historial_tickets = fields.One2many(
        'helpdesk.ticket', 'Tickets anteriores', compute="_get_historial_tickets")
    #historial_tickets = fields.One2many('helpdesk.ticket')
