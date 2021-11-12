# -*- coding: utf-8 -*-

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    role_ids = fields.One2many('project.scrum.role', 'employee_id',
                                string = "Team Role", tracking=True, help="Link to scrum role.")
