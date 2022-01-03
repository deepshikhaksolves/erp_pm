# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

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
    ks_project_type_id = fields.Many2one('ks.project.type', string='Project Type',
                                         related='project_id.ks_project_type')
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
    ks_uat_date = fields.Date(string='UAT End Date', required=True,
                              copy=False)
    ks_bug_fix_date = fields.Date(string='Bug fixes Date', copy=False)
    ks_internal_eta_date = fields.Date(string='Internal ETA Date', required=True,
                                       copy=False)
    ks_internal_sow_date = fields.Date(string='Internal SOW Date', required=True,
                                       copy=False)
    ks_internal_qa_date = fields.Date(string='Internal QA Date', required=True,
                                      copy=False)
    ks_internal_delivery_date = fields.Date(string='Internal Delivery/Deployment Date',
                                            required=True, copy=False)
    # ks_internal_uat_date = fields.Date(string='Internal UAT Date', required=True,
    #                                    copy=False)
    ks_internal_bug_fix_date = fields.Date(string='Internal Bug fixes Date', copy=False)
    ks_project_sprint_checklist_ids = fields.One2many('ks.sprint.checklist', 'sprint_id',
                                                      string="Documents", help="Link to Sprint Checklist.")
    ks_doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    product_owner_id = fields.Many2one(
        'res.users',
        'Product Owner',
        related='project_id.product_owner_id',
        domain=lambda self: [('groups_id', 'in', self.env.ref(
            'project_scrum_agile.group_scrum_owner').ids)],
        help="The person who is responsible for the product"
    )
    scrum_master_id = fields.Many2one(
        'res.users',
        'Scrum Master',
        related='project_id.scrum_master_id',
        domain=lambda self: [('groups_id', 'in', self.env.ref(
            'project_scrum_agile.group_scrum_master').ids)],
        help="The person who maintains the process for the product"
    )
    # @api.constrains('ks_sprint_code', 'name')
    # def create_project_sprint_sequence(self):
    #     """For creating project sequence on create of project.
    #     This runs on create, write and duplicating record."""
    #     if self.ks_sprint_code and self.name:
    #         ks_sprint_code = self.ks_sprint_code.upper()
    #         if self.project_id:
    #             if self.project_id.is_scrum:
    #                 # Create project sprint sequence if not a scrum project.
    #                 project_sprint = self.project_id.ks_short_code.upper() + ' - ' + ks_sprint_code
    #                 seq = self.env['ir.sequence'].create({
    #                     "name": "Project %s - Sprint %s Sequence" % (self.project_id.name, self.name),
    #                     "code": "project.project %s" % ks_sprint_code,
    #                     "prefix": "(# %s - " % project_sprint,
    #                     "suffix": ")",
    #                     "padding": 3
    #                 })
    #                 self.ks_sprint_sequence_id = seq.id
    #             else:
    #                 raise ValidationError(
    #                     _("Project related to this sprint doesn't have scrum option enable. "))
    #         else:
    #             raise ValidationError(
    #                 _("Please add project in this sprint."))

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

    def attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['domain'] = str([('id', 'in', self.ks_project_sprint_checklist_ids.mapped('attachment').ids)])
        return action

    def _compute_attached_docs_count(self):
        for scrum_sprint in self:
            scrum_sprint.ks_doc_count = len(self.ks_project_sprint_checklist_ids.mapped('attachment').ids)

    """ Scheduler for sprint build reminder """
    @api.model
    def reminder_sprint_build(self):
        try:
            tomorrow = datetime.now() + timedelta(1)
            sprint_rec = self.env['project.scrum.sprint'].sudo().search([])
            for rec in sprint_rec:
                to_email_list = rec.project_id.team_id.employee_ids.mapped('work_email')
                if rec.product_owner_id:
                    to_email_list.append(rec.product_owner_id.employee_ids.work_email)
                if rec.project_id.product_owner_id:
                    to_email_list.append(rec.project_id.product_owner_id.employee_ids.work_email)
                if rec.scrum_master_id:
                    to_email_list.append(rec.scrum_master_id.employee_ids.work_email)
                email = set(to_email_list)
                to_email_ids = ",".join(email)
                if str(rec.ks_internal_qa_date) == tomorrow.strftime('%Y-%m-%d'):
                    template = self.env.ref('ks_project_scrum.build_reminder_mail_template')
                    mail = self.env['mail.template'].browse(template.id).with_context(email_to=to_email_ids).send_mail(rec.id, force_send=False)

        except Exception as e:
            print("Sprint Build cron error: ", e)
            pass
    
    """ Scheduler for sprint delivery reminder """
    @api.model
    def reminder_sprint_delivery(self):
        try:
            tomorrow = datetime.now() + timedelta(1)
            sprint_rec = self.env['project.scrum.sprint'].sudo().search([])
            for rec in sprint_rec:
                to_email_list = rec.project_id.team_id.employee_ids.mapped('work_email')
                if rec.product_owner_id:
                    to_email_list.append(rec.product_owner_id.employee_ids.work_email)
                if rec.project_id.product_owner_id:
                    to_email_list.append(rec.project_id.product_owner_id.employee_ids.work_email)
                if rec.scrum_master_id:
                    to_email_list.append(rec.scrum_master_id.employee_ids.work_email)
                email = set(to_email_list)
                to_email_ids = ",".join(email)
                if str(rec.ks_internal_delivery_date) == tomorrow.strftime('%Y-%m-%d'):
                    template = self.env.ref('ks_project_scrum.sprint_delivery_reminder_mail_template')
                    mail = self.env['mail.template'].browse(template.id).with_context(email_to=to_email_ids).send_mail(rec.id, force_send=False)

        except Exception as e:
            print("Sprint Delivery cron error: ", e)
            pass

    """ Scheduler for Sprint Client UAT reminder """
    @api.model
    def reminder_sprint_uat(self):
        try:
            tomorrow = datetime.now() + timedelta(1)
            sprint_rec = self.env['project.scrum.sprint'].sudo().search([])
            for rec in sprint_rec:
                to_email_list = rec.project_id.team_id.employee_ids.mapped('work_email')
                if rec.product_owner_id:
                    to_email_list.append(rec.product_owner_id.employee_ids.work_email)
                if rec.project_id.product_owner_id:
                    to_email_list.append(rec.project_id.product_owner_id.employee_ids.work_email)
                if rec.scrum_master_id:
                    to_email_list.append(rec.scrum_master_id.employee_ids.work_email)
                email = set(to_email_list)
                to_email_ids = ",".join(email)
                if str(rec.ks_uat_date) == tomorrow.strftime('%Y-%m-%d'):
                    template = self.env.ref('ks_project_scrum.sprint_uat_reminder_mail_template')
                    mail = self.env['mail.template'].browse(template.id).with_context(email_to=to_email_ids).send_mail(rec.id, force_send=False)

        except Exception as e:
            print("Client UAT cron error: ", e)
            pass

    """ Scheduler for Client Delivery reminder """
    @api.model
    def reminder_client_delivery(self):
        try:
            tomorrow = datetime.now() + timedelta(1)
            sprint_rec = self.env['project.scrum.sprint'].sudo().search([])
            for rec in sprint_rec:
                to_email_list = rec.project_id.team_id.employee_ids.mapped('work_email')
                if rec.product_owner_id:
                    to_email_list.append(rec.product_owner_id.employee_ids.work_email)
                if rec.project_id.product_owner_id:
                    to_email_list.append(rec.project_id.product_owner_id.employee_ids.work_email)
                if rec.scrum_master_id:
                    to_email_list.append(rec.scrum_master_id.employee_ids.work_email)
                email = set(to_email_list)
                to_email_ids = ",".join(email)
                if str(rec.ks_delivery_date) == tomorrow.strftime('%Y-%m-%d'):
                    template = self.env.ref('ks_project_scrum.client_delivery_reminder_mail_template')
                    mail = self.env['mail.template'].browse(template.id).with_context(email_to=to_email_ids).send_mail(rec.id, force_send=False)

        except Exception as e:
            print("Client Delivery cron error: ", e)
            pass
