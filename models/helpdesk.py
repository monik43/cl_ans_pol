# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class helpdesk_stage(models.Model):
    _inherit = "helpdesk.stage"

    sla_id = fields.Many2one("helpdesk.sla", "Politica ANS")
    def_assign = fields.Many2one("res.users", "Técnico")


class helpdesk_ticket(models.Model):
    _inherit = "helpdesk.ticket"

    def _get_historial_tickets(self):
        for ticket in self:
            for t in (
                self.env["helpdesk.ticket"]
                .with_context(active_test=False)
                .search([("x_lot_id.id", "=", ticket.x_lot_id.id)])
            ):
                if t.id != ticket.id and (t.active in (True, False)):
                    ticket.update({"historial_tickets": [(4, t.id)]})

    historial_tickets = fields.One2many(
        "helpdesk.ticket",
        string="Tickets anteriores",
        compute="_get_historial_tickets",
        context={"active_test": False},
    )
    # historial_tickets = fields.One2many('helpdesk.ticket')

    @api.onchange("stage_id")
    def onchange_stage_id_eq_sla_id(self):
        for ticket in self:
            # asignacion politica ans correcta
            if not ticket.stage_id.sla_id and self.env["helpdesk.sla"].search(
                [("name", "=", ticket.stage_id.name)]
            ):
                ticket.sla_id = self.env["helpdesk.sla"].search(
                    [("name", "=", ticket.stage_id.name)]
                )
            elif ticket.stage_id.sla_id:
                ticket.sla_id = ticket.stage_id.sla_id
            # asignacion usuario x defecto
            if (
                ticket.stage_id.def_assign
                and ticket.user_id != ticket.stage_id.def_assign
            ):
                ticket.user_id = ticket.stage_id.def_assign


    # team_id -> siempre el mismo
    # priority -> no relevante
    # ticket_type_id -> no usado
    # create_date
    @api.depends('team_id', 'priority', 'ticket_type_id', 'create_date')
    def _compute_sla(self):
        if not self.user_has_groups("helpdesk.group_use_sla"):
            return
        for ticket in self:
            print(f"ticket.team_id.id -> {ticket.team_id}, priority -> {ticket.priority}, ticket.ticket_type_id -> {ticket.ticket_type_id}")
            print("/"*50)
            dom = [('team_id', '=', ticket.team_id.id), ('priority', '<=', ticket.priority), '|', ('ticket_type_id', '=', ticket.ticket_type_id.id), ('ticket_type_id', '=', False)]
            sla = ticket.env['helpdesk.sla'].search(dom, order="time_days, time_hours", limit=1)
            working_calendar = self.env.user.company_id.resource_calendar_id
            print(f"sla -> {sla}, working_calendar -> {working_calendar}")
            print("/"*50)
            if sla and ticket.sla_id != sla and ticket.active and ticket.create_date:
                ticket.sla_id = sla.id
                ticket.sla_name = sla.name
                ticket_create_date = fields.Datetime.from_string(ticket.create_date)
                if sla.time_days > 0:
                    deadline = working_calendar.plan_days(
                        sla.time_days+1,
                        ticket_create_date,
                        compute_leaves=True)
                    # We should also depend on ticket creation time, otherwise for 1 day SLA for example all tickets
                    # created on monday will have the deadline as tuesday 8:00
                    deadline = deadline.replace(hour=ticket_create_date.hour, minute=ticket_create_date.minute, second=ticket_create_date.second, microsecond=ticket_create_date.microsecond)
                else:
                    deadline = ticket_create_date
                # We should execute the function plan_hours in any case because
                # if i create a ticket for 1 day sla configuration and tomorrow at the same time i don't work,
                # deadline falls on the time that i don't work which is ticket creation time and is not correct
                ticket.deadline = working_calendar.plan_hours(
                    sla.time_hours,
                    deadline,
                    compute_leaves=True)

    @api.multi
    def open_ticket(self):
        for rec in self:
            url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            rec_url = (
                url
                + "/web#id="
                + str(self.id)
                + "&view_type=form&model=helpdesk.ticket"
            )
            client_action = {
                "type": "ir.actions.act_url",
                "name": self.display_name,
                "target": "new",
                "url": rec_url,
            }

            return client_action
