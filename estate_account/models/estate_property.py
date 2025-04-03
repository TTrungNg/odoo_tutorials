from odoo import Command, models
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"


    def action_sold(self):
        invoice_vals = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100,
                }),
            ],
        }
        empty_invoice = self.env['account.move'].create(invoice_vals)
        return super().action_sold()

