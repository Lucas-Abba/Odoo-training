from datetime import timedelta
from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_round

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'property model'
    _order = 'id desc'

    name = fields.Char(required=True, default="Unknown")
    tags_id = fields.Many2many('estate.property.tag')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=91))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer()
    garage = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area(sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('weast', 'Weast')])
    total_area = fields.Integer(compute='_compute_total', string='Total Area(sqm)')
    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)   
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', copy=False)
    best_price = fields.Float( string='Best Offer', compute='_compute_best_price', default='0')
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled'),], default='new')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'A property expected price must be strictly positive'),
         ('check_selling_price', 'CHECK(selling_price > 0)',
         'A property selling price must be positive'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.offer_ids and float_compare(record.selling_price, (record.expected_price * 0.9), 2) == -1:
                raise ValidationError("Selling price can't be lower than than $" + str(record.expected_price * 0.9))



    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in (self):
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in (self):
            if record.offer_ids:
                record.best_price = max( offer.price for offer in record.offer_ids)
            else:
                record.best_price = 0



    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''


    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled' :
                raise exceptions.UserError("Cancelled properties can't be sold.")
            else:    
                record.state = 'sold'
            return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold' :
                raise exceptions.UserError("Sold properties can't be cancelled")
            else:
                record.state = 'cancelled'
            return True

