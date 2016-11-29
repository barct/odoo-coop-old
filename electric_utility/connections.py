# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from debug import oprint

class Sector(models.Model):
	_name="electric_utility.sector"

	code = fields.Char("Code", length=7)
	name = fields.Char("Name")

	_sql_constraints = [('sector_unique_keys', 'unique(code)', 'Code must be unique!'),]


class Connection(models.Model):
	_name = "electric_utility.connection"
	
	number = fields.Integer("Connection N°", required=True)
	sector = fields.Many2one("electric_utility.sector", "Sector", required=True)
	measurement_sequence = fields.Float("Measurement Sequence")

	
	service_address_street = fields.Char("Street", required=True)
	service_address_neighborhood = fields.Char("Neighborhood")
	service_address_city = fields.Char("City", required=True)
	service_address_lat = fields.Float("Latitude")
	service_address_lng = fields.Float("Longitude")
	cadastral_nomenclature = fields.Char("Cadastral Nomenclature")

	_sql_constraints = [('connection_unique_keys', 'unique(number)', 'Code must be unique!'),]


class Contrat(models.Model):

	_name = "electric_utility.contrat"

	date_start = fields.Date("Date Start", required=True)
	date_end = fields.Date("Date End")

	connection_id = fields.Many2one("res.partner", "Connection", required=True)
	client_id = fields.Many2one("res.partner", "Client", required=True)

	service_category_id = fields.Many2one("electric_utility.service_category", "Service Category", required=True)
	installed_potency = fields.Integer("Installed Potency")
	delivery_sequence = fields.Float("Selivery Sequence")
