# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_TASK_STATE = [
    ("draft", "New"),
    ("open", "In Progress"),
    ("pending", "Pending"),
    ("done", "Done"),
    ("cancelled", "Cancelled"),
]


class Project(models.Model):
    _inherit = "project.project"

    ks_project_type = fields.Many2one('ks.project.type', string='Project Type', required=True)
    ks_billing_type = fields.Selection([('Fixed', 'Fixed Project'),
                                        ('Monthly', 'TnM Project')], string="Billing Type")
    ks_short_code = fields.Char(string="Short Code", required=True,
                                help="This code will be used on tasks being created for this project.")
    ks_project_sequence_id = fields.Many2one(comodel_name='ir.sequence', string="Project Sequence")
    _sql_constraints = [('uniq_name', 'unique(ks_short_code)',
                         "A Short code already exists with this name . Short Code name must be unique!"),
                        ]
    project_start_date = fields.Date(string='Project Start Date')
    project_end_date = fields.Date(string='Project End Date')
    state = fields.Selection(_TASK_STATE)

    @api.constrains('ks_short_code', 'name')
    def create_project_sequence(self):
        """For creating project sequence on create of project.
        This runs on create, write and duplicating record."""
        if self.ks_short_code and self.name:
            ks_short_code = self.ks_short_code.upper()
            if not self.is_scrum:
                # Create project sequence if not a scrum project.
                seq = self.env['ir.sequence'].create({
                    "name": "Project %s Sequence" % self.name,
                    "code": "project.project %s" % ks_short_code,
                    "prefix": "(#%s - " % ks_short_code,
                    "suffix": ")",
                    "padding": 3
                })
                self.ks_project_sequence_id = seq.id

    @api.model
    def create(self, vals):
        """Add project followers."""
        res = super(Project, self).create(vals)
        team_id = vals.get('team_id')
        #    Add customer, project owner and scrum master as follower.
        for user_id in [vals.get('partner_id'), vals.get('product_owner_id'),
                        vals.get('scrum_master_id')]:
            if user_id:
                res.env['mail.followers'].sudo().create({'res_model': 'project.project',
                                                          'partner_id': user_id,
                                                          'res_id': res.id})
        if team_id:
            team = res.env['project.scrum.devteam'].browse(team_id)
            if team.employee_ids:
                # Add new followers from team.
                for team_member in team.employee_ids:
                    res.message_follower_ids = [(0, 0, {'res_model': 'project.project',
                                                        'partner_id': team_member.user_partner_id.id})]

            else:
                raise ValidationError(_("No Team member is added in team!.."))

        return res

    def write(self, vals):
        """Update project followers if team is changed."""
        res = super(Project, self).write(vals)
        team_id = vals.get('team_id')
        if team_id or vals.get('partner_id') or vals.get('scrum_master_id')or vals.get('product_owner_id'):
            # if team_id:
            # Remove the existing followers
            existing_followers = self.env['mail.followers'].search([
                ('res_id', '=', self.id),
                ('res_model', '=', 'project.project')])
            existing_followers.unlink()
            #    Add customer, project owner and scrum master as follower.
            self.env['mail.followers'].sudo().create({
                'res_model': 'project.project',
                'partner_id': self.partner_id.id,
                'res_id': self.id})

            for user_id in [self.product_owner_id, self.scrum_master_id]:
                if user_id:
                    self.env['mail.followers'].sudo().create({
                        'res_model': 'project.project',
                        'partner_id': user_id.partner_id.id,
                        'res_id': self.id})
            if team_id:
                team = self.env['project.scrum.devteam'].browse(team_id)
                if team.employee_ids:
                    # Add new followers from team.
                    for team_member in team.employee_ids:
                        self.env['mail.followers'].sudo().create({
                            'res_model': 'project.project',
                            'partner_id': team_member.user_partner_id.id,
                            'res_id': self.id})
                else:
                    raise ValidationError(_("No Team member is added in team!.."))

        return res

    def unlink(self):
        """Remove followers when record is deleted for a project."""
        res = super(Project, self).unlink()
        existing_followers = self.env['mail.followers'].search([
            ('res_id', '=', self.id),
            ('res_model', '=', 'project.project')])
        return res
