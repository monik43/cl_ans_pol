# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import date, datetime, time, timedelta
import pytz
from odoo import api, fields, models, _


class mail_activity(models.Model):
    _inherit = "mail.activity"

    @api.onchange('activity_type_id','user_id')
    def _onchange_activity_type_id(self):
        if self.activity_type_id and self.user_id:
            self.summary = self.activity_type_id.summary
            tz = self.user_id.sudo().tz
            laborables = tuple()

            for dia in self.user_id.resource_calendar_id.attendance_ids:
                laborables += (int(dia.dayofweek),)
            print(f"lab dow: {laborables}")

            if tz:
                today_utc = pytz.UTC.localize(datetime.utcnow())
                today = today_utc.astimezone(pytz.timezone(tz))
            else:
                today = datetime.now()

            date_deadline = (today + timedelta(days=self.activity_type_id.days))

            if date_deadline.weekday() not in laborables:
                for day in range(1,7):
                    ndt = date_deadline + timedelta(days=day)
                    if ndt.weekday() in laborables:
                        print(ndt.weekday(), " is laborable")
                        break
            else:
                print("dt in laborables")
            print("end")

            #self.date_deadline = ###
            self.date_deadline = (today + timedelta(days=self.activity_type_id.days))
            
