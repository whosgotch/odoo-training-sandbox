from odoo import models, fields, api


class EstatePropertyType(models.Model):
    # Private fields
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Property type must be unique.")
    ]
    
    # Default fields
    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=1)

    # Relational fields
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", compute="_compute_offer"
    )

    # Compute fields
    offer_count = fields.Integer(compute="_compute_offer")

    # Compute methods
    def _compute_offer(self):
        offer_count = {}
        offer_ids = {}

        offers = self.env["estate.property.offer"].search(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)]
        )

        for offer in offers:
            property_type_id = offer.property_type_id.id
            if property_type_id not in offer_count:
                offer_count[property_type_id] = 0
                offer_ids[property_type_id] = []
            offer_count[property_type_id] += 1
            offer_ids[property_type_id].append(offer.id)

        for prop_type in self:
            prop_type.offer_count = offer_count.get(prop_type.id, 0)
            prop_type.offer_ids = offer_ids.get(prop_type.id, [])
