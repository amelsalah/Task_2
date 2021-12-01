# -*- coding: utf-8 -*-

from odoo import models, fields



class Services(models.Model):
    _name = 'services'

    name = fields.Char(required=True,translate=True)
    logo = fields.Binary(string="Service Logo")
   