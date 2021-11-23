# -*- coding: utf-8 -*-

from odoo import fields, models


class KsProjectScrumRole(models.Model):
    _inherit = ['project.scrum.role', 'mail.thread']
    _name = 'project.scrum.role'

    designation_id = fields.Many2one('ks.role.designation',
                                     string="Designation", tracking=True,
                                     help="Designation of employee for the linked project.")
    name = fields.Char('Designation Name', required=False, related="designation_id.name")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  tracking=True, help="Employee")
    person_name = fields.Char(string='Employee Name', related='employee_id.name',
                              help="Person name as employee's name.")
    scrum_devteam_id = fields.Many2one('project.scrum.devteam',
                                       string="Scrum Development Team", tracking=True,
                                       help="Link the employee and designation with a team.")
    employee_image = fields.Binary(related='employee_id.image_1920', tracking=True,
                                   help="Linked employee's avatar/image.")
