from odoo import api, fields, models, tools
from odoo import exceptions
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "list all the properties for estate"
    _order = "id desc"

    name = fields.Char(required=True)
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default=('new'),
        selection=[
            ('new', 'New'), 
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
    description = fields.Text()
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    buyer = fields.Many2one("res.partner", copy=False)
    seller = fields.Many2one("res.users", string = "Salesman", index = True, tracking = True, default = lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default = fields.Date.today() + relativedelta(months=3), string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Determine which orientation of the estate")
    
    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be positive.'),
        ('positive_selling_price', 'CHECK(selling_price > 0)',
         'The selling price must be positive.'),
    ]

    total_area = fields.Integer(compute='_compute_total_area')
    best_offer = fields.Float(compute='_compute_best_offer')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0)
    
    @api.onchange("garden")
    def _onchang_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
            return {'warning': {
                'title': ("Warning"),
                'message': ('This option has cleared Garden Area and Orientation')}}
        
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_vs_expected_price(self):
        for property in self:
            if not (tools.float_utils.float_is_zero(property.selling_price, precision_rounding=0.01)):
                if tools.float_utils.float_compare(property.selling_price/property.expected_price, 0.9,precision_digits=2) == -1:
                    raise exceptions.ValidationError("Selling price cannot be lower than 90% of the expected price")

        
    def action_sold(self):
        for property in self:
            if property.state == "cancelled":
                raise exceptions.UserError('Cancelled property cannot be Sold.')
            else:
                property.state = "sold"
        return True
    
    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise exceptions.UserError('Sold property cannot be Cancelled.')
            else:
                property.state = "cancelled"
        return True
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_canceled(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise exceptions.UserError("Can only delete New or Canceled properties!")























