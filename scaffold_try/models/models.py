# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class scaffold_try(models.Model):
#     _name = 'scaffold_try.scaffold_try'
#     _description = 'scaffold_try.scaffold_try'
    # def create(self):
    # 	# put your codes here
    #     return super().create()

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields

class EstatePropertyTagInherit(models.Model):
    _inherit = "estate.property.tag"

    priority = fields.Integer(string="Tag Priority", default=0)
    color = fields.Integer(string="Color Index Overide field", required=True)

class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

    client_document_number = fields.Char(string="SO Client Number")