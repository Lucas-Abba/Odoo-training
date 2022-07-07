from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = 'Property tags'
    _order = 'name asc'

    name = fields.Char(required=True, default="Unknown")


    _sql_constraints = [
        ('tag_name_uniq', 'unique (name)',
        'A property tag name must be unique')
    ]
    