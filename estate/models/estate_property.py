from odoo import models, fields, api

class EstateProperty(models.Model):
  _name = 'estate.property'
  _description = 'Real Estate Property'

  name = fields.Char(required=True)
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date(copy=False, default=(fields.Date.add(fields.Date.today(), months=+3)))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly=True, copy=False)
  bedrooms = fields.Integer(default=2)
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
  active = fields.Boolean(default=True)
  state = fields.Selection(required=True, default='new', selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')])
  property_type_id = fields.Many2one("estate.property.type", string="Property Type")
  buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
  salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
  tags_ids = fields.Many2many("estate.property.tag", string="Property Tags")
  offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
  total_area = fields.Integer(compute="_compute_total_area")
  best_price = fields.Integer(compute="_compute_best_price")

  @api.depends("living_area", "garden_area")
  def _compute_total_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area

  @api.depends("offer_ids.price")
  def _compute_best_price(self):
    for line in self:
        if line.offer_ids:
          line.best_price = max(line.mapped("offer_ids.price")) or 0
        else:
          line.best_price = 0

  @api.onchange("garden")
  def _onchange_garden(self):
    if self.garden:
      self.garden_area = 10 
      self.garden_orientation = "north"
    else:
      self.garden_area = 0
      self.garden_orientation = ""