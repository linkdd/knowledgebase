# -*- coding: utf-8 -*-

from wtforms import Form, IntegerField, validators


class WalkForm(Form):

    LOOKUP_VERTICES = 0
    LOOKUP_EDGES = 1
    LOOKUP_BOTH = 2

    depth = IntegerField('Walk depth', [
        validators.DataRequired(),
        validators.NumberRange(min=1)
    ])
    lookup = IntegerField('Type of elements to return', [
        validators.AnyOf([LOOKUP_VERTICES, LOOKUP_EDGES, LOOKUP_BOTH])
    ], default=LOOKUP_BOTH)
