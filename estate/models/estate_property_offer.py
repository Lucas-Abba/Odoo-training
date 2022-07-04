from datetime import timedelta, date, datetime
from email.policy import default
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'offer for a property'

    price = fields.Float(required=True, default='0')
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer( default='7', string='Validity(days)')
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')



    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------


    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in (self):
            if (record.create_date):
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    @api.depends('date_deadline', 'validity')
    def _inverse_deadline(self):
        for record in (self):
            if (record.create_date):
                record.validity =  (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - date.today()).days


    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------


    #TODO change criteria of decide if an offer is refused of accepted

    def action_confirm_offer(self):
        for record in (self):
            if record.status == 'accepted':
                print("    This offer is already Accepted")
            elif (record.property_id.buyer_id):
                print("    An offer is already Accepted")
            else:
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.status = 'accepted'
        return True

    def action_refuse_offer(self):
        for record in (self):
            if record.status == 'refused':
                print("    This offer is already Refused")
            elif (record.status == 'accepted'):
                print("    This offer has been already Accepted")
            else:
                record.status = 'refused'
        return True