# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class KsSprintCheckListOption(models.Model):
    _name = 'ks.sprint.checklist.option'
    _description = 'Sprint Checklist Option'

    name = fields.Char(string='Name')
    ks_project_type_id = fields.Many2one('ks.project.type', string='Project Type')
    visible_to_manager = fields.Boolean(string='Visible To Scrum Master')


class KsSprintCheckList(models.Model):
    _name = 'ks.sprint.checklist'
    _description = 'Sprint Checklist'

    @api.onchange('project_type')
    def _onchange_project_type(self):
        """Method to return Sprint Checklist Option ids with some conditions. """
        if self.project_type:
            if self.env.user.has_group('project_scrum_agile.group_scrum_master') or \
                    self.env.user.has_group('project_scrum_agile.group_scrum_owner'):
                rec = self.env['ks.sprint.checklist.option'].sudo().search(['|', ('ks_project_type_id', '=', False),
                                                                            ('ks_project_type_id', '=',
                                                                            self.project_type.id)])
            else:
                rec = self.env['ks.sprint.checklist.option'].sudo().search([('visible_to_manager', '=', False), '|',
                                                                            ('ks_project_type_id', '=', False),
                                                                            ('ks_project_type_id', '=',
                                                                            self.project_type.id)])
            return {'domain': {'name': [('id', 'in', rec.ids)]}}
        else:
            return False

    sprint_id = fields.Many2one('project.scrum.sprint', string='Sprint', required=True)
    project_type = fields.Many2one('ks.project.type', related='sprint_id.ks_project_type_id')
    name = fields.Many2one('ks.sprint.checklist.option', string='Name')

    attachment = fields.One2many('ir.attachment', 'ks_sprint_checklist_id', ondelete='cascade')
    is_completed = fields.Boolean('Done')


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    ks_sprint_checklist_id = fields.Many2one('ks.sprint.checklist')
