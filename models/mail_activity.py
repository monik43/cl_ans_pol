# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import date, datetime, time, timedelta
import pytz
from odoo import api, fields, models, _


class mail_activity(models.Model):
    _inherit = "mail.activity"

    @api.onchange('activity_type_id, user_id')
    def _onchange_activity_type_id(self):
        if self.activity_type_id:
            self.summary = self.activity_type_id.summary
            tz = self.user_id.sudo().tz
            if tz:
                today_utc = pytz.UTC.localize(datetime.utcnow())
                today = today_utc.astimezone(pytz.timezone(tz))
            else:
                today = datetime.now()

        #dt = datetime.strptime(values_w_defaults['date_deadline'], '%Y-%m-%d')
        laborables = tuple()
        """for dia in self.env['res.users'].browse(values_w_defaults['user_id']).resource_calendar_id.attendance_ids:
            laborables += (int(dia.dayofweek),)
        print(dt, laborables)

        if dt.weekday() not in laborables:
            for day in range(1,7):
                ndt = dt + timedelta(days=day)
                print(f"Dia: {ndt.weekday()}")
                if ndt.weekday() in laborables:
                    print(ndt.weekday(), " is laborable")
                    break
        else:
            print("dt in laborables")
        print("end")"""

        print((today + timedelta(days=self.activity_type_id.days)).weekday(), "/"*25)
        self.date_deadline = (
            today + timedelta(days=self.activity_type_id.days))
