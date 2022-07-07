from email.policy import default
from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'property type'
    _order = 'name asc'

    name = fields.Char(required=True, default="Unknown")
    property_ids = fields.One2many('estate.property', 'property_type_id', readonly=True)
    sequence = fields.Integer('Sequence', default=1, help='Used to order property types.')

    _sql_constraints = [
        ('type_name_uniq', 'unique (name)',
        'A property type name must be unique')
    ]


    