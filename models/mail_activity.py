# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import date, datetime, time, timedelta
import pytz
from odoo import api, fields, models, _

class mail_activity_type(models.Model):
    _inherit = "mail.activity.type"

    default_user_id = fields.Many2one('res.users', 'Asignado por defecto a', domain=[('share','=',False)])

class mail_activity(models.Model):
    _inherit = "mail.activity"

    #@api.onchange('activity_type_id','user_id'). ahora sin user_id
    @api.onchange('activity_type_id')
    def onchange_activity_type_id(self):
        if self.activity_type_id and self.user_id:
            self.summary = self.activity_type_id.summary
            tz = self.user_id.sudo().tz
            laborables = tuple()
            # planificacion en dias laborables del trabajador

            # - recoleccion días de la semana que trabaja el usuario 
            for dia in self.user_id.resource_calendar_id.attendance_ids:
                laborables += (int(dia.dayofweek),)

            if tz:
                today_utc = pytz.UTC.localize(datetime.utcnow())
                today = today_utc.astimezone(pytz.timezone(tz))
            else:
                today = datetime.now()

            date_deadline = (today + timedelta(days=self.activity_type_id.days))

            # - si date_deadline cae en fin de semana o en un dia que no trabaje el usuario,
            #   empieza la busqueda del siguiente dia laborable 
            if date_deadline.weekday() not in laborables:
                for day in range(1,8):
                    ndt = date_deadline + timedelta(days=day)
                    if ndt.weekday() in laborables:
                        date_deadline = ndt
                        break

            self.date_deadline = date_deadline
            
            # asignacion usuario x defecto de cada tipo de planificacion
            if self.activity_type_id.default_user_id:
                self.user_id = self.activity_type_id.default_user_id
            

            
