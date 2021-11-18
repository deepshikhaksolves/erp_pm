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
    ks_sprint_code = fields.Char(string="Sprint code", required=True)
    _sql_constraints = [('uniq_name', 'unique(ks_sprint_code)',
                         "A Sprint code already exists with this name. Sprint Code name must be unique!"),
                        ]
    ks_sprint_sequence_id = fields.Many2one(comodel_name='ir.sequence', string="Sprint Sequence")
    release_id = fields.Many2one('project.scrum.release', string='Release',
                                 copy=False)
    ks_eta_date = fields.Date(string='ETA Date', required=True,
                              copy=False)
    ks_sow_date = fields.Date(string='SOW Date', required=True,
                              copy=False)
    ks_qa_date = fields.Date(string='QA Date', required=True,
                             copy=False)
    ks_delivery_date = fields.Date(string='Delivery/Deployment Date',
                                   required=True, copy=False)
    ks_uat_date = fields.Date(string='UAT Date', required=True,
                              copy=False)
    ks_bug_fix_date = fields.Date(string='Buf fixes Date', copy=False)
    ks_internal_eta_date = fields.Date(string='Internal ETA Date', required=True,
                                       copy=False)
    ks_internal_sow_date = fields.Date(string='Internal SOW Date', required=True,
                                       copy=False)
    ks_internal_qa_date = fields.Date(string='Internal QA Date', required=True,
                                      copy=False)
    ks_internal_delivery_date = fields.Date(string='Internal Delivery/Deployment Date',
                                            required=True, copy=False)
    ks_internal_uat_date = fields.Date(string='Internal UAT Date', required=True,
                                       copy=False)
    ks_internal_bug_fix_date = fields.Date(string='Internal Bug fixes Date', copy=False)

    @api.constrains('ks_sprint_code', 'name')
    def create_project_sprint_sequence(self):
        """For creating project sequence on create of project.
        This runs on create, write and duplicating record."""
        if self.ks_sprint_code and self.name:
            ks_sprint_code = self.ks_sprint_code.upper()
            if self.project_id:
                if self.project_id.is_scrum:
                    # Create project sprint sequence if not a scrum project.
                    project_sprint = self.project_id.ks_short_code.upper() + ' - ' + ks_sprint_code
                    seq = self.env['ir.sequence'].create({
                        "name": "Project %s - Sprint %s Sequence" % (self.project_id.name, self.name),
                        "code": "project.project %s" % ks_sprint_code,
                        "prefix": "(# %s - " % project_sprint,
                        "suffix": ")",
                        "padding": 1
                    })
                    self.ks_sprint_sequence_id = seq.id
                else:
                    raise ValidationError(
                        _("Project related to this sprint doesn't have scrum option enable. "))
            else:
                raise ValidationError(
                    _("Please add project in this sprint."))

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
