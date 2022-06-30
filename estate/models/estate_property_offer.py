from datetime import timedelta, datetime
from email.policy import default
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'offer for a property'

    price = fields.Float(required=True, default='0')
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
    # validity = fields.Integer( default='7', string='Validity(days)')
    # date_deadline = fields.Date(compute='_compute_deadline')



    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------


    # @api.depends('create_date', 'validity')
    # def _compute_deadline(self):
    #     for record in (self):
    #         if (record.create_date):
    #             record.date_deadline = record.create_date + timedelta(days=record.validity)
    #         else:
    #             record.date_deadline = datetime.now() + timedelta(days=record.validity)
    