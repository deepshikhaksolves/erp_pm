# -*- coding: utf-8 -*-

from odoo import api, fields, models


class KsProjectScrumDevteam(models.Model):
    _inherit = ['project.scrum.devteam', 'mail.thread']
    _name = 'project.scrum.devteam'

    scrum_team_member_ids = fields.One2many('project.scrum.role', 'scrum_devteam_id',
                                            "Team Members", tracking=True, help="Link to scrum role.")
    employee_ids = fields.Many2many('hr.employee', string='Employee Ids')

    @api.onchange('scrum_team_member_ids')
    def _onchange_team_member(self):
        employee_list = self.scrum_team_member_ids.mapped('employee_id').ids
        self.update({'employee_ids': [( 6, 0, employee_list)]})