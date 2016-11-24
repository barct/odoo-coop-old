# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from datetime import date
from openerp.osv import fields as old_fields
from minutes import minutes


class Member(models.Model):
    _inherit = "res.partner"

    membership_number = fields.Integer(string='Membership N', default=None)
    admission_minutes_id = fields.Many2one('minutes','Admission Minutes')
    affiliation_date = fields.Date(string="Affiliation Date")
    disaffiliation_date = fields.Date(string="Disffiliation Date")
    disaffiliation_minutes_id = fields.Many2one('minutes',string='Disaffiliation Minutes')
    reasons_for_disaffiliation = fields.Char(string="Reasons for Disaffiliation ")
    
