from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property type must be unique.')
    ]