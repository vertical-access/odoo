# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Project(models.Model):

    _name = "project.project"
    _inherit = [
        'project.project',
        'mail.activity.mixin',
        ]

    @api.model
    def create(self, vals):
        # we grab some custom values from the order
        vals = self._get_order_info(vals)
        # we grab the related task types defined as default
        project_type_id = vals.get('type_id',False)
        stages = self.env["project.task.type"].search([("case_default", "=", True),("default_project_type_id", "=", project_type_id)])
        if stages:
            vals['type_ids'] = [(6,0,stages.ids)]
        
        return super(Project, self).create(vals)
    
    @api.model
    def _get_order_info(self, vals):
        if vals.get('sale_order_id'):
            so = self.env['sale.order'].browse(vals['sale_order_id'])
            if so.project_type_id:
                vals['type_id'] = so.project_type_id.id
        
        return vals

