# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from dbfread import DBF
import hashlib
#from openerp.tools.config import config
#from datetime import date
#from openerp.osv import fields as old_fields

#class suscriptor(models.Model):
#	hashcode = fields.Char(length=15)


class TableSync():
	"""
	Class TableSync
		is a base class for mirroring dbf of Infcooop system... and other stuff 
	"""
	hashcode = fields.Char(length=15)
	dbf_table = None

	def __init__(self, *args, **kwargs):
		super(TableSync, self).__init__(*args,**kwargs)
		

	def generateHash(self, rowdata):
		"""
		generate a hash code based on a raw row
		"""
		hash = hashlib.sha1()
		hash.update(str(rowdata))
		self.hashcode=hash.hexdigest()[-10:]
		return self.hashcode

	def checkHash(self, rowdata):
		"""
		check if row data maches the hash
		"""
		hash = hashlib.sha1()
		hash.update(str(rowdata))
		if self.hashcode==hash.hexdigest()[-10:]:
			return True
		else:
			return False

	def dbf_rows(self):
		"""
		iterate in every rows
		This method should be overwritten in a subclass to filter rows
		"""
		for row in self.dbf_table:
				yield row
	
	def sync(self, env):
		"""
		here's the magic
		Gets all rows in the dbf file and verifies that they are loaded in the model
		"""
		model = str(self)
		path = self.pool.get("infocoop_configuration").get_dbf_path()
		dbf_tablename = path + "/" + self.dbf_tablename + '.dbf'
		self.dbf_table = DBF(dbf_tablename)
		for row in self.dbf_rows():
			pklist = []
			for pk in self.dbf_pk:
				pklist.append(pk,"=",row[pk.upper()])

			ids = env[model].search(pklist)
			if ids:
				is_changed = not (ids[0].checkHash(unicode(row)))
				if is_changed:
					ids[0].write_row(row, self.dbf_table)
			else:
				new = env[model].create({})
				new.write_row(row, self.dbf_table)


	def write_row(self, dbf_row, dbf_table):
		'''
		write dbf row in the model
		'''
		write_dict={}
		for f in dbf_table.fields:
			write_dict[f.name.lower()]=dbf_row[f.name.upper()]
		self.write(write_dict)
		self.generateHash(unicode(dbf_row))
			


class infocoop_ingresos(models.Model, TableSync):
	'''
	This model is a mirror of a table ingresos in InfoCoop system
	ingresos represent the members in a cooperative
	Not to be confused with socios table. This last one represent a service connections
	(... yes, this guys are awesome :O )
	'''

	dbf_tablename = "ingresos"
	dbf_pk = ("socio","medidor","orden")

	nombre = fields.Char(string='nombre',length=30)
	cuotas = fields.Integer(string='cuotas')
	pesos = fields.Float(string='pesos')
	contado = fields.Float(string='contado')
	cuotas_men = fields.Integer(string='cuotas_men')
	profesion = fields.Char(string='profesion',length=30)
	nacionalid = fields.Char(string='nacionalid',length=15)
	tipo_doc = fields.Integer(string='tipo_doc')
	nro_doc = fields.Char(string='nro_doc')
	telefono = fields.Char(string='telefono',length=15)
	dirser = fields.Char(string='dirser',length=30)
	domicilio = fields.Char(string='domicilio',length=60)
	localidad = fields.Integer(string='localidad')
	fec_nacim = fields.Date(string='fec_nacim')
	estado_civ = fields.Integer(string='estado_civ')
	padre = fields.Char(string='padre',length=30)
	madre = fields.Char(string='madre',length=30)
	conyugue = fields.Char(string='conyugue',length=30)
	sector = fields.Integer(string='sector')
	socio = fields.Integer(string='socio', index=True)
	acta = fields.Integer(string='acta')
	fec_acta = fields.Date(string='fec_acta')
	fec_ingr = fields.Date(string='fec_ingr')
	observacio = fields.Text(string='observacio')
	aceptado = fields.Boolean(string='aceptado')
	barrio = fields.Integer(string='barrio')
	medidor = fields.Integer(string='medidor')
	orden = fields.Char(string='orden',length=1)
	fec_baja = fields.Date(string='fec_baja')
	codpostal = fields.Char(string='codpostal',length=15)
	sexo = fields.Char(string='sexo',length=1)


	def dbf_rows(self):
		for row in super(infocoop_ingresos, self).dbf_rows():
			if row["FEC_BAJA"] is None:
				yield row
