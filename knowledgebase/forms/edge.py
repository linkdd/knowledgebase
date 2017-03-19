# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class EdgeForm(Form):
    source = StringField('Source Vertex', [
        validators.DataRequired()
    ])
    target = StringField('Target Vertex', [
        validators.DataRequired()
    ])
    type = StringField('Edge type', [
        validators.DataRequired()
    ])
    name = StringField('Edge name', [
        validators.DataRequired()
    ])
