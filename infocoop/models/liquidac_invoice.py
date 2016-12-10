# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from suscriber import Suscriber
from debug import oprint


from utils import doc_number_normalize, name_clean


class LiquidacInvoice(models.Model, Suscriber):
	_name = "infocoop.liquidac_invoice"
	
	master_id = fields.Many2one('infocoop_liquidac', ondelete='cascade')
	slave_id = fields.Many2one('account.invoice')
	
	def prepare_row_fields(self, row):
		
		partner_id = 11 ## TODO
		journal_id = 3
		internal_number = "DV/2016/" + str(row.numero), #TODO: get journal book
		period_id = 12 ##get from settlements

		return {
		"number": internal_number , #TODO: get journal book
		"supplier_invoice_number": internal_number,
		"company_id": self.env.user.company_id.id,
		"currency_id": self.env.user.company_id.currency_id.id,
		"amount_untaxed": row.neto_serv,
		"amount_tax": row.neto_imp,
		"amount_total": row.neto_serv + row.neto_imp,
		"partner_id": partner_id,
		"commercial_partner_id": partner_id,
		"journal_id": journal_id,
		"state": "open",
		#"type": "out_invoice",
		"internal_number":  internal_number,
		"date_invoice": None, ##TODO: get from settlements
		"sent": False,
		"period_id": period_id,
		"afip_document_class_id": 6, #TODO: create a settlwmwnts type
		"afip_document_number": "0001" + str(row.numero),
		"journal_document_class_id": 3,
		"responsability_id": 6,

				}
	