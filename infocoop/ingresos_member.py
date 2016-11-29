# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from debug import oprint
import re
from utils import doc_number_normalize

def name_clean(name):
	names = name.split("-")
	name=names[0]
	name = re.sub('[*]', '', name)
	name = re.sub('\s+', ' ', name)
	return name.title()


class IngresosMember(models.Model):
	_name = "infocoop.ingresos_member"
	
	master_id = fields.Many2one('infocoop_ingresos', ondelete='cascade')
	slave_id = fields.Many2one('res.partner', ondelete='cascade')
	hashcode = fields.Char(length=10)

	_sql_constraints = [('unique_keys', 'unique(master_id,slave_id)', 'must be unique!'),]

	def create_from_infocoop(self, row):
		new = self.env['res.partner'].create((self.prepare_row_fields(row)))
		self.create({"slave_id":new.id, "master_id": row.id, "hashcode": row.hashcode})

	def update_from_infocoop(self, row):
		self.slave_id.write(self.prepare_row_fields(row))
		self.hashcode=row.hashcode

	def prepare_row_fields(self, row):
		doc_type, doc_number = doc_number_normalize(row.tipo_doc, row.nro_doc)
		
		#TODO: This could be more efficient
		ids = self.env["afip.document_type"].search((["active","=",True],["code","=",doc_type]), limit=1)
		if ids:
			doc_type=ids[0].id
		else:
			doc_type=None

		minutes_id = None
		if row.acta:
			minutes_id = self.env["minutes"].search((["number","=",row.acta],), limit=1).id
			if not minutes_id:
				minutes_id= self.env["minutes"].create({"number":row.acta, "date":row.fec_acta}).id




		localidad = self.env["infocoop_tablas"].search((["tema","=","T"],["subtema","=","L"],["codigo","=",row.localidad]), limit=1)
		if localidad:
			city = localidad["concepto"].title()
		else:
			city = None

		return {
			"name": name_clean(row.nombre),
			"document_number": doc_number,
			"document_type_id": doc_type,
			"birthdate": row.fec_nacim,
			"affiliation_date": row.fec_ingr,
			"membership_number": row.socio,
			"phone": row.telefono,
			"comment": row.observacio,
			"admission_minutes_id": minutes_id,
			"city": city,
			"street": row.domicilio,
			"zip": row.codpostal,
			"responsability_id": "res_CF",
			}