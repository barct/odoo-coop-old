# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from debug import oprint


class Measurements(models.Model):
	_name = "electric_utility.measurement"

	