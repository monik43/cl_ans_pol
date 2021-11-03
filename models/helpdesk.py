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
            for tic in ticket.historial_tickets:
                if tic.x_lot_id.id != ticket.x_lot_id.id:
                    ticket.update({"historial_tickets": [(3, tic.id)]})

    historial_tickets = fields.One2many(
        "helpdesk.ticket",
        string="Tickets anteriores",
        compute="_get_historial_tickets",
        context={"active_test": False},
    )
    # historial_tickets = fields.One2many('helpdesk.ticket')
    last_deadline = fields.Datetime(string="Last deadline")

    @api.onchange("x_lot_id")
    def onchange_x_lot_id_unlink(self):
        for ticket in self:
            for tic in ticket.historial_tickets:
                if tic.x_lot_id.id != ticket.x_lot_id.id:
                    ticket.update({"historial_tickets": [(3, tic.id)]})

    @api.onchange("stage_id")
    def onchange_stage_id_eq_sla_id(self):
        self.last_deadline = self.deadline

        self.env.cr.execute(
            f"""SELECT stage_id
                FROM helpdesk_ticket 
                WHERE id = {self._origin.id};"""
        )
        ret = self.env.cr.fetchone()[0]
        if isinstance(ret, int):
            print(f"""
                    browse -> {self.env["helpdesk.stage"].browse(ret).name}
                    self -> {self._origin.stage_id.name}
                    """,)
        # if sequencia actual < sequencia anterior and han pasado menos de 6h del anterior cambio de estado
        # ticket._compute_sla()

    @api.depends("stage_id", "create_date")
    def _compute_sla(self):
        if not self.user_has_groups("helpdesk.group_use_sla"):
            return
        for ticket in self:
            sla = self.env["helpdesk.sla"].search(
                [("stage_id", "=", ticket.stage_id.id)]
            )
            working_calendar = self.env.user.company_id.resource_calendar_id
            # asignacion politica ans correcta
            if sla and ticket.sla_id != sla and ticket.active:
                ticket.sla_id = sla.id
                ticket.sla_name = sla.name
                ticket_deadline_date = fields.Datetime.from_string(
                    fields.Datetime.now()
                )
                if sla.time_days > 0:
                    deadline = working_calendar.plan_days(
                        sla.time_days + 1, ticket_deadline_date, compute_leaves=True
                    )
                    deadline = deadline.replace(
                        hour=ticket_deadline_date.hour,
                        minute=ticket_deadline_date.minute,
                        second=ticket_deadline_date.second,
                        microsecond=ticket_deadline_date.microsecond,
                    )
                else:
                    deadline = ticket_deadline_date
                ticket.deadline = working_calendar.plan_hours(
                    sla.time_hours, deadline, compute_leaves=True
                )
                # asignacion usuario x defecto
            if (
                ticket.stage_id.def_assign
                and ticket.user_id != ticket.stage_id.def_assign
            ):
                ticket.user_id = ticket.stage_id.def_assign

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
