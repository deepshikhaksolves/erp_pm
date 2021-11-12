# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import date


class KSPublicHolidaysLine(models.Model):
    _name = 'public.holidays'
    _description = 'Public Holidays Lines'

    year = fields.Integer(
        "Calendar Year",
        required=True,
        default=date.today().year
    )
    line_ids = fields.One2many(
        'public.holidays_lines',
        'year_id',
        'Holiday Dates'
    )

    def name_get(self):
        res = []
        for rec in self:
            ks_name = str(rec.year)
            res.append((rec.id, ks_name))
        return res


class KSPublicHolidaysLineIds(models.Model):
    _name = 'public.holidays_lines'
    _description = 'display public holidays'
    _order = 'date asc'

    name = fields.Char(
        'Name',
        required=True,
    )
    date = fields.Date(
        'Date',
        required=True
    )
    year_id = fields.Many2one(
        'public.holidays',
        'Calendar Year',
        required=True,
    )