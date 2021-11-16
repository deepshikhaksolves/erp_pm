# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class KsProjectScrumRelease(models.Model):
    _inherit = 'project.scrum.release'

    sprint_release_tasks_count = fields.Integer("Tasks", compute='get_sprint_release_tasks_count')

    def ks_sprint_release_tasks(self):
        print(self)
        return {
            'name': _('Scrum Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'domain': [('release_id', '=', self.id)],
        }

    def get_sprint_release_tasks_count(self):
        count = self.env['project.task'].search_count([('release_id', '=', self.id)])
        self.sprint_release_tasks_count = count


class KsProjectScrumSprint(models.Model):
    _inherit = 'project.scrum.sprint'

    sprint_tasks_count = fields.Integer(string="Tasks",
                                        compute='get_sprint_tasks_count')
    release_id = fields.Many2one('project.scrum.release',
                                 string='Release', copy=False)
    ks_eta_date = fields.Date(string='ETA Date', readonly=True,
                              required=True, copy=False)
    ks_sow_date = fields.Date(string='SOW Date', readonly=True,
                              required=True, copy=False)
    ks_qa_date = fields.Date(string='QA Date', readonly=True,
                             required=True, copy=False)
    ks_delivery_date = fields.Date(string='Delivery/Deployment Date', readonly=True,
                                   required=True, copy=False)
    ks_uat_date = fields.Date(string='UAT Date', readonly=True,
                              required=True, copy=False)
    ks_bug_fix_date = fields.Date(string='Buf fixes Date', readonly=True,
                                  copy=False)
    ks_internal_eta_date = fields.Date(string='Internal ETA Date', readonly=True,
                                       required=True, copy=False)
    ks_internal_sow_date = fields.Date(string='Internal SOW Date', readonly=True,
                                       required=True, copy=False)
    ks_internal_qa_date = fields.Date(string='Internal QA Date', readonly=True,
                                      required=True, copy=False)
    ks_internal_delivery_date = fields.Date(string='Internal Delivery/Deployment Date',
                                            readonly=True, required=True, copy=False)
    ks_internal_uat_date = fields.Date(string='Internal UAT Date', readonly=True,
                                       required=True, copy=False)
    ks_internal_bug_fix_date = fields.Date(string='Internal Bug fixes Date', readonly=True,
                                           copy=False)

    def ks_sprint_tasks(self):
        return {
            'name': _('Scrum Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph,activity',
            'domain': [('sprint_id', '=', self.id)],
        }

    def get_sprint_tasks_count(self):
        count = self.env['project.task'].search_count([('sprint_id', '=', self.id)])
        self.sprint_tasks_count = count

    @api.constrains('release_id')
    def check_sprint_release_exist(self):
        """To check the value of release is not repeated in sprint again."""
        if self.release_id:
            if len(self.release_id.sprint_ids.ids) > 1:
                raise ValidationError(
                    _("This release is already linked with another sprint. Please create a new release with this "
                      "sprint."))
