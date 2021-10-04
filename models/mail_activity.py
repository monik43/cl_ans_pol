# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import date, datetime, time, timedelta
from odoo import api, fields, models, _


class mail_activity(models.Model):
    _inherit = "mail.activity"

    @api.model
    def create(self, values):
        # already compute default values to be sure those are computed using the current user
        values_w_defaults = self.default_get(self._fields.keys())
        values_w_defaults.update(values)
        dt = datetime.strptime(values_w_defaults['date_deadline'], '%Y-%m-%d')
        laborables = tuple()
        for dia in self.env['res.users'].browse(values_w_defaults['user_id']).resource_calendar_id.attendance_ids:
            laborables += (int(dia.dayofweek),)
        print(dt, laborables)

        if dt.weekday() not in laborables:
            for day in range(1,7):
                ndt = dt + timedelta(days=day)
                print(f"Dia: {ndt.weekday()}")
                if ndt in laborables:
                    print(ndt.weekday(), " is laborable")
        else:
            print("dt in laborables")
        # continue as sudo because activities are somewhat protected
        activity = super(mail_activity, self.sudo()).create(values_w_defaults)
        activity_user = activity.sudo(self.env.user)
        activity_user._check_access('create')
        self.env[activity_user.res_model].browse(activity_user.res_id).message_subscribe(partner_ids=[activity_user.user_id.partner_id.id])
        if activity.date_deadline <= fields.Date.today():
            self.env['bus.bus'].sendone(
                (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                {'type': 'activity_updated', 'activity_created': True})
        return activity_user