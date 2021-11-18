# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        """Get project task number on task create."""
        if not vals.get('task_number'):
            if self.project_id:
                # If scrum project get sequence from
                if self.project_id.is_scrum and self.sprint_id:
                    sequence_code = self.sprint_id.ks_project_sequence_id.code
                    vals['task_number'] = self.env['ir.sequence'].next_by_code(
                        sequence_code) or '/'
                elif not self.project_id.is_scrum:
                    sequence_code = self.project_id.ks_project_sequence_id.code
                    vals['task_number'] = self.env['ir.sequence'].next_by_code(
                        sequence_code) or '/'
                else:
                    raise ValidationError(_("Please add sprint in this task."))

            else:
                raise ValidationError(_("Please add project in this task."))
        return super(ProjectTask, self).create(vals)