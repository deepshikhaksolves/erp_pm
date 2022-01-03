# -*- coding: utf-8 -*-

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    role_ids = fields.One2many('project.scrum.role', 'employee_id',
                                string = "Team Role", tracking=True, help="Link to scrum role.")

    # def create(self, vals):
    #     """Create a employee when user is created."""
    #     res = super(Project, self).create(vals)
    #     res.action_create_employee()
    #     return res
