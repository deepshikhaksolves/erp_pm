# -*- coding: utf-8 -*-

from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    ks_project_type = fields.Many2one('ks.project.type', string='Project Type')
    ks_billing_type = fields.Selection([('Fixed', 'Fixed'),
                                        ('Monthly', 'Monthly')], string="Billing Type")
