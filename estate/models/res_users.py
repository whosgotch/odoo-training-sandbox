from odoo import fields, models


class ResUsers(models.Model):
    # Private fields
    _inherit = "res.users"

    # Relational fields
    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )
