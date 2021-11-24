# -*- coding: utf-8 -*-

from odoo import fields, models


class KsSprintCheckListOption(models.Model):
    _name = 'ks.sprint.checklist.option'
    _description = 'Sprint Checklist Option'

    name = fields.Char(string='Name')
    ks_project_type_id = fields.Many2one('ks.project.type', string='Project Type')


class KsSprintCheckList(models.Model):
    _name = 'ks.sprint.checklist'
    _description = 'Sprint Checklist'

    name = fields.Char(string='Name')
    sprint_id = fields.Many2one('project.scrum.sprint', string='Sprint', required=True)
    related_document_type = fields.Selection([('url', 'URL'), ('attachment', 'Attachment')],
                                             string='Related Document Type', required=True)


