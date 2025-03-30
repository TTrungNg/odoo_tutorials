from odoo import api, fields, models, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers of estate property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy = False,
        selection = [
            ('accepted', 'Accepted'), 
            ('refused', 'Refused'),
        ]
    )
    partner_id = fields.Many2one('res.partner', required = True, string = "Partner")
    property_id = fields.Many2one('estate.property', required = True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)',
         'The offer price must be positive.'),
    ]

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Datetime.now()) + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = (offer.create_date or fields.Datetime.now()).date()
            offer.validity = (offer.date_deadline - create_date).days

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.state = 'offer accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
        return True
    
    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if property.offer_ids and vals['price'] < max(property.offer_ids.mapped("price")):
                raise exceptions.UserError("You have to add a higher offer")
            property.state = "offer received"
        return super().create(vals_list)

