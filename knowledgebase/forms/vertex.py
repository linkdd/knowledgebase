# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class VertexForm(Form):
    type = StringField('Edge type', [
        validators.DataRequired()
    ])
    name = StringField('Edge name', [
        validators.DataRequired()
    ])
