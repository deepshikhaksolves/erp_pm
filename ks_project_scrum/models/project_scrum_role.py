# -*- coding: utf-8 -*-

from odoo import fields, models


class KsProjectScrumRole(models.Model):
    _inherit = 'project.scrum.role'

    name = fields.Char(string='Designation Name', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    person_name = fields.Char(string='Employee Name', related='employee_id.name')
    scrum_devteam_id = fields.Many2one('project.scrum.devteam', string="Scrum Development Team")
    image_1920 = fields.Image(related='employee_id.image_1920')
