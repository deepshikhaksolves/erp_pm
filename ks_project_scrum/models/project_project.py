# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    ks_project_type = fields.Many2one('ks.project.type', string='Project Type')
    ks_billing_type = fields.Selection([('Fixed', 'Fixed'),
                                        ('Monthly', 'Monthly')], string="Billing Type")
    ks_short_code = fields.Char(string="Short Code", required=True,
                                help="This code will be used on tasks being created for this project.")
    ks_project_sequence_id = fields.Many2one(comodel_name='ir.sequence', string="Project Sequence")
    _sql_constraints = [('uniq_name', 'unique(ks_short_code)',
                         "A Short code already exists with this name . Short Code name must be unique!"),
                        ]

    @api.constrains('ks_short_code', 'name')
    def create_project_sequence(self):
        """For creating project sequence on create of project.
        This runs on create, write and duplicating record."""
        if self.ks_short_code and self.name:
            ks_short_code = self.ks_short_code.upper()
            if not self.is_scrum:
                # Create project sequence if not a scrum project.
                seq = self.env['ir.sequence'].create({
                    "name": "Project %s Sequence" % self.name,
                    "code": "project.project %s" % ks_short_code,
                    "prefix": "(#%s - " % ks_short_code,
                    "suffix": ")",
                    "padding": 1
                })
                self.ks_project_sequence_id = seq.id