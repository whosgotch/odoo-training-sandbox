from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Offer price of property must be positive.'),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for line in self:
            line.date_deadline = fields.Date.add(line.create_date or fields.Date.today(), days=line.validity)

    def _inverse_date_deadline(self):
        for line in self:
            line.validity = (line.date_deadline - line.create_date.date() or fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Offer is already accepted!")
            
            else:
                record.status = "accepted" 
                record.property_id.state = "offer accepted"
                record.property_id.selling_price = record.price 
                record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0
            record.property_id.buyer_id = ""

    @api.model
    def create(self, vals):
        if vals.get("property_id"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            prop.state = "offer received"
        return super().create(vals)
    