from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of estate property"
    _order = "name"

    name = fields.Char(required = True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count')
    sequence = fields.Integer("Sequence", default=1, help="Used to order Property types. Lower is better.")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
