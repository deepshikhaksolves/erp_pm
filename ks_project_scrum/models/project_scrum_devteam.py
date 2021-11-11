# -*- coding: utf-8 -*-

from odoo import fields, models


class KsProjectScrumRole(models.Model):
    _inherit = 'project.scrum.devteam'

    scrum_team_member_ids = fields.One2many('project.scrum.role', 'scrum_devteam_id', "Team Members")