# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from suscriber import Suscriber
from debug import oprint
import datetime


from utils import doc_number_normalize, name_clean


class LiquidacInvoice(models.Model, Suscriber):
	_name = "infocoop.liquidac_invoice"
	
	master_id = fields.Many2one('infocoop_liquidac', ondelete='cascade')
	slave_id = fields.Many2one('account.invoice')
	
	
	def prepare_row_fields(self, row):
		
		##get journal
		journal_id = self.env["infocoop_configuration"].get_liquidac_invoice_journal_id()
		if not journal_id:
			raise Exception("Liquidac to Invoice Journal must be configurated")

		#get client_id
		contrat = self.env["electric_utility.contrat"].search([("contrat_number","=",str(row.medidor)+str(row.orden)),],limit=1)
		if contrat:
			partner_id = contrat.client_id
		else:
			raise Exception("Contrat %s%s not found" % (row.medidor,row.orden))

		#desagrego periodo
		_sp =  row.periodo.split("/")
		month=int(_sp[0])
		year = int(_sp[1])
		period_date = datetime.date(year=year, month=month, day=1)
		period_id = self.env["account.period"].search([("date_start","<=",period_date),],limit=1, order="date_start desc").id

		#internal_number = "DV/2016/" + str(row.numero), #TODO: get journal book
		afip_document_class = self.env.ref('electric_utility.dc_b_lsp')
		journal_document_class = self.env["account.journal.afip_document_class"].search([("afip_document_class_id","=",afip_document_class.id),],limit=1)

		prefix = journal_document_class.sequence_id.prefix

		sequence = journal_id.sequence_id
		d = sequence._interpolation_dict()
		interpolated_prefix = sequence._interpolate(sequence['prefix'], d)
		interpolated_suffix = sequence._interpolate(sequence['suffix'], d)
		internal_number = interpolated_prefix + '%%0%sd' % sequence['padding'] % row.numero + interpolated_suffix

		return {
		"number": internal_number , #TODO: get journal book
		#"supplier_invoice_number": internal_number,
		"company_id": self.env.user.company_id.id,
		"currency_id": self.env.user.company_id.currency_id.id,
		"amount_untaxed": row.neto_serv,
		"amount_tax": row.neto_imp,
		"amount_total": row.neto_serv + row.neto_imp,
		"partner_id": partner_id.id,
		"commercial_partner_id": partner_id.id,
		"journal_id": journal_id.id,
		"state": "draft",
		"account_id":contrat.account_id.id,
		#"type": "out_invoice",
		"internal_number":  internal_number,
		"date_invoice": period_date, ##TODO: get from settlements
		"sent": False,
		"period_id": period_id,
		"afip_document_class_id": afip_document_class.id,
		"afip_document_number": str(prefix) + str(row.numero),
		"journal_document_class_id": journal_document_class.id,
		"responsability_id": partner_id.responsability_id.id,

		}



	def get_slave_form_row(self, row):
		#desagrego periodo
		_sp =  row.periodo.split("/")
		month=int(_sp[0])
		year = int(_sp[1])
		period_date = datetime.date(year=year, month=month, day=1)
		period_id = self.env["account.period"].search([("date_start","<=",period_date),],limit=1, order="date_start desc").id

		return self.env["account.invoice"].search([("contrat_id.contrat_number","=",str(row.medidor)+str(row.orden)),("period_id","=",period_id)], limit=1)	

	