# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)
from debug import oprint


class infocoop_configuration(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = "infocoop_configuration"

    dbf_path = fields.Char(string="Path to dbfs")

    otra_opcion = fields.Boolean(string="Otra Opción")

    @api.multi
    def get_default_dbf_path(self, fields):
        #print(self.dbf_path)
        #oprint(self.search_read([],"dbf_path"))
      
        return {
            'dbf_path': "/tmp",
        }

    def get_dbf_path(self):
        return "/var/lib/odoo/virt-env/server/sources/odoo-coop/infocoop/data/dbfs"

    @api.multi
    def sync_tables(self, *args, **kwargs):
        ts = self.pool('infocoop_ingresos')
        ts.sync(self.env, *args, **kwargs)
    