# -*- coding: utf-8 -*-

from odoo import fields, models


class KsProjectType(models.Model):
    _name = 'ks.project.type'
    _description = 'Project Type'

    name = fields.Char(string='Name')