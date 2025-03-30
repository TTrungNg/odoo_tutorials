from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of estate property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
    _sql_constraints = [
        ('unique_name_tag', 'UNIQUE(name)',
         'Property Tags must be unique.'),
    ]