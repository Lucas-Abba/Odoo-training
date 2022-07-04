from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'property type'

    name = fields.Char(required=True, default="Unknown")

    _sql_constraints = [
        ('type_name_uniq', 'unique (name)',
        'A property type name must be unique')
    ]


    