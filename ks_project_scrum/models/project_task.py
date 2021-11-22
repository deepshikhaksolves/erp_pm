# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Removed related ids from both sprint_id and release_id fields.
    sprint_id = fields.Many2one(
        'project.scrum.sprint',
        'Sprint',
        store=True
    )
    release_id = fields.Many2one(
        'project.scrum.release',
        'Release',
        store=True
    )

    @api.model
    def create(self, vals):
        """Get project task number on task create."""
        res = super(ProjectTask, self).create(vals)
        # project_latest_sprint_id = self.env['project.scrum.sprint'].search([(
        #     'project_id', '=', res.project_id.id)], limit=1).id
        # # To pick last sprint if not selected.
        # if not res.sprint_id:
        #     res.sprint_id = project_latest_sprint_id
        if res.task_number == '/':
            if res.project_id:
                # If scrum project get sequence from
                if res.project_id.is_scrum and res.sprint_id:
                    sequence_code = res.sprint_id.ks_sprint_sequence_id.code
                    res.task_number = res.env['ir.sequence'].next_by_code(
                        sequence_code) or '/'
                elif not res.project_id.is_scrum:
                    sequence_code = res.project_id.ks_project_sequence_id.code
                    res.task_number = res.env['ir.sequence'].next_by_code(
                        sequence_code) or '/'
                else:
                    raise ValidationError(_("Please add sprint in this task."))

            else:
                raise ValidationError(_("Please add project in this task."))
        return res