from odoo import models, fields


class EstatePropertyTag(models.Model):
    # Private fields
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [("unique_name", "UNIQUE(name)", "Property tag must be unique.")]

    # Default fields
    name = fields.Char(required=True)
    color = fields.Integer()
    
