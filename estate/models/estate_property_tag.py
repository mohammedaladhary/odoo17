from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index")

    def property_xlsx_report(self):
        # print('hello')
        return {
            'type': 'ir.actions.act_url',
            'url': f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }