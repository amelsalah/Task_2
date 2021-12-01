# -*- coding: utf-8 -*-

from odoo import models, fields



class ClientsRequests(models.Model):
    _name = 'clients.requests'

    partner_id = fields.Many2one('res.partner')
    name = fields.Char(related='partner_id.name')
    phone = fields.Char(related='partner_id.phone')
    email = fields.Char(related='partner_id.email')
    description = fields.Text()
    service_id = fields.Many2one('services')