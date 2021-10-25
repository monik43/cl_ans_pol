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
            for t in self.env['helpdesk.ticket'].with_context(active_test=False).search(['|', ('x_sn', '=', ticket.x_sn), ('x_lot_id.id', '=', ticket.x_lot_id.id)]):
                if t.id != ticket.id and (t.active in (True, False)):
                    ticket.update({'historial_tickets': [(4, t.id)]})

    historial_tickets = fields.One2many(
        'helpdesk.ticket', string='Tickets anteriores', compute="_get_historial_tickets",  context={'active_test': False})
    #historial_tickets = fields.One2many('helpdesk.ticket')

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
                ticket.user_id = ticket.stage_id.def_assign

    
    

    @api.multi
    def open_ticket(self):
        for rec in self:
            url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            rec_url = (
                url + "/web#id=" + str(self.id) + "&view_type=form&model=helpdesk.ticket"
            )
            client_action = {
                "type": "ir.actions.act_url",
                "name": self.display_name,
                "target": "new",
                "url": rec_url,
            }

            return client_action
