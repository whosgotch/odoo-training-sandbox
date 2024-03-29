from odoo import models, fields, Command


class EstateProperty(models.Model):
    # Private fields
    _inherit = "estate.property"    

    # Action methods
    def action_sell_property(self):
        res = super().action_sell_property()
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": prop.name,
                                "quantity": 1.0,
                                "price_unit": prop.selling_price * 6.0 / 100.0,
                            },
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                }
            )
        return res
