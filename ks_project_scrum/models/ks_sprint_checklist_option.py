# -*- coding: utf-8 -*-

from odoo import api, fields, models


class KsSprintCheckListOption(models.Model):
    _name = 'ks.sprint.checklist.option'
    _description = 'Sprint Checklist Option'

    name = fields.Char(string='Name')
    ks_project_type_id = fields.Many2one('ks.project.type', string='Project Type')
    visible_to_manager = fields.Boolean(string='Visible To Manager')

class KsSprintCheckList(models.Model):
    _name = 'ks.sprint.checklist'
    _description = 'Sprint Checklist'

    @api.model
    def _domain_get_ids(self):
        if self.env.user.has_group('project.group_project_manager'):
            rec = self.env['ks.sprint.checklist.option'].sudo().search([('visible_to_manager', '=', True)])
        else:
            rec = self.env['ks.sprint.checklist.option'].sudo().search([])
        return [('id', 'in', rec.ids)]

    sprint_id = fields.Many2one('project.scrum.sprint', string='Sprint', required=True)
    project_type = fields.Many2one('ks.project.type', related='sprint_id.ks_project_type_id')
    # name = fields.Many2one('ks.sprint.checklist.option', string='Name', domain="['|', ('ks_project_type_id', '=', "
    #                                                                            "False), ('ks_project_type_id', '=', "
    #                                                                            "project_type)]")
    name = fields.Many2one('ks.sprint.checklist.option', string='Name', domain=_domain_get_ids)

    attachment = fields.One2many('ir.attachment', 'ks_sprint_checklist_id', ondelete='cascade')
    is_completed = fields.Boolean('Done')


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    ks_sprint_checklist_id = fields.Many2one('ks.sprint.checklist')
