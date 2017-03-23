# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class VertexForm(Form):
    type = StringField('Vertex type', [
        validators.DataRequired()
    ])
    name = StringField('Vertex name', [
        validators.DataRequired()
    ])
