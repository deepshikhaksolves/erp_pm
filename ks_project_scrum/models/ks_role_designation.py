# -*- coding: utf-8 -*-

from odoo import fields, models


class KsRoleDesignation(models.Model):
    _name = 'ks.role.designation'
    _description = 'Role Designation'

    name = fields.Char(string='Name')