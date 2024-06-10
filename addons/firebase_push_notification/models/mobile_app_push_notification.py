from odoo import models, fields, api, _
import requests

from odoo.exceptions import UserError, ValidationError

import firebase_admin
from firebase_admin import credentials, messaging
import os
import logging
_logger = logging.getLogger(__name__)

class MobileAppPushNotification(models.Model):
    _name = 'mobile.app.push.notification'
    _description = 'Push Notification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _order = 'id desc'

    STATE_SELECTION = [
        ('draft', 'Draft'),
        ('done', 'Sent'),
        ('Planned', 'Planned'),
        ('cancel', 'Cancel'),
        ('error', 'Error'),
    ]
    data = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'serviceAccountKey.json'))
    cred = credentials.Certificate(data)
    
    firebase_admin.initialize_app(cred)

    name = fields.Char('Title', tracking=True)
    body = fields.Text('Message', tracking=True)
    send_notification_to = fields.Selection([('to_all','All Partners'),('to_specefic','To a partner')], string='Send To', default='to_all', tracking=True)

    log_history = fields.One2many('push.notification.log.history', 'notification_id', 'History', )
    partner_ids = fields.Many2many('res.partner', string="User")
    state = fields.Selection(STATE_SELECTION, 'Status', readonly=False, default='draft', tracking=True)

    def send_notification(self):
        tokens = []
        partner_ids = self.env['res.partner'].search([])
        if self.send_notification_to == 'to_all':
            for rec in partner_ids:
                for line in rec.mail_firebase_tokens:
                    tokens.append({'partner_id': line.partner_id.id, 'token': line.token})
        else:
            for rec in self.partner_ids:
                for line in rec.mail_firebase_tokens:
                    tokens.append({'partner_id': line.partner_id.id, 'token': line.token})

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=self.name or '',
                body=self.body or '',
            ),
            data=None,
            tokens=[item['token'] for item in tokens],
        )
        response = messaging.send_multicast(message)
        
        if response:
            self.env['push.notification.log.history'].sudo().create({
                'notification_id': self.id,
                'date_send': fields.Datetime.now(),
                'notification_state': 'success',
            })
            responses = response.responses
            failed_tokens = []
            success_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    failed_tokens.append(tokens[idx])
                if resp.success:
                    success_tokens.append(tokens[idx])

            for succ in success_tokens:
                self.env['push.notification.log.partner'].sudo().create({
                    'notification_id': self.id,
                    'name': self.name,
                    'body': self.body,
                    'partner_id': succ['partner_id'],
                    'date_send': fields.Datetime.now(),
                    'notification_state': 'success',
                    'device_token': succ['token'],
                })
            self.write({'state': 'done'})
            for succ in failed_tokens:
                self.env['push.notification.log.partner'].sudo().create({
                    'notification_id': self.id,
                    'name': self.name,
                    'body': self.body,
                    'partner_id': succ['partner_id'],
                    'date_send': fields.Datetime.now(),
                    'notification_state': 'failed',
                    'device_token': succ['token'],
                })

    def set_to_draft(self):
        self.write({'state': 'draft'})

class PushNotificationLogHistory(models.Model):
    _name = 'push.notification.log.history'
    _description = 'Push Notification'

    notification_id = fields.Many2one('mobile.app.push.notification')
    date_send = fields.Datetime("Send Date")
    notification_state = fields.Selection([('success', 'Success'), ('failed', 'Failed')], string="State")
