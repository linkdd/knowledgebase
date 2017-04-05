# -*- coding: utf-8 -*-
# Inspired from https://github.com/zbyte64/wtforms-jsonschema

from collections import OrderedDict
from inspect import isclass


def pretty_name(name):
    """Converts 'first_name' to 'First name'"""

    if not name:
        return u''

    return name.replace('_', ' ').capitalize()


class WTFormToJSONSchema(object):
    DEFAULT_CONVERSIONS = {
        'URLField': {
            'type': 'string',
            'format': 'uri'
        },
        'URIField': {
            'type': 'string',
            'format': 'uri'
        },
        'URIFileField': {
            'type': 'string',
            'format': 'uri',
            'ux-widget': 'file-select' #not part of spec but flags behavior
        },
        'FileField': {
            'type': 'string',
            'format': 'uri',
            'ux-widget': 'file-select' #not part of spec but flags behavior
        },
        'DateField': {
            'type': 'string',
            'format': 'date'
        },
        'DateTimeField': {
            'type': 'string',
            'format': 'datetime'
        },
        'DecimalField': {
            'type': 'number'
        },
        'IntegerField': {
            'type': 'integer'
        },
        'BooleanField': {
            'type': 'boolean'
        },
        'StringField': {
            'type': 'string'
        },
        'SearchField': {
            'type': 'string'
        },
        'TelField': {
            'type': 'string',
            'format': 'phone'
        },
        'EmailField': {
            'type': 'string',
            'format': 'email'
        },
        'DateTimeLocalField': {
            'type': 'string',
            'format': 'datetime'
        },
        'ColorField': {
            'type': 'string',
            'format': 'color'
        },
        #TODO min/max
        'DecimalRangeField': {
            'type': 'number'
        },
        'IntegerRangeField': {
            'type': 'integer'
        },
    }

    INPUT_TYPE_MAP = {
        'text': 'StringField',
        'checkbox': 'BooleanField',
        'color': 'ColorField',
        'tel': 'TelField'
    }

    def __init__(
        self,
        form,
        conversions=None,
        include_array_item_titles=True,
        include_array_title=True,
        forms_seen=None,
        json_schema=None,
        path=None,
        *args, **kwargs
    ):
        super(WTFormToJSONSchema, self).__init__(*args, **kwargs)

        self.conversions = conversions or self.DEFAULT_CONVERSIONS
        self.include_array_item_titles = include_array_item_titles
        self.include_array_title = include_array_title

        self.form = form
        self.forms_seen = {}
        self.json_schema = {
            'type': 'object',
            'properties': OrderedDict()
        }
        self.path = []

        if forms_seen is not None:
            self.forms_seen = forms_seen

        if json_schema is not None:
            self.json_schema = json_schema

        if path is not None:
            self.path = path

        key = id(self.form)

        if key in self.forms_seen:
            self.json_schema['$ref'] = '#{0}'.format(
                '/'.join(self.forms_seen[key])
            )
            self.json_schema.pop('properties', None)

        else:
            self.forms_seen[key] = self.path

        if isclass(self.form):
            self.form = self.form()
            fields = [
                name
                for name, ufield in self.form._unbound_fields
            ]

        else:
            fields = self.form._fields.keys()

        for name in fields:
            if name not in self.form._fields:
                continue

            field = self.form._fields[name]
            self.json_schema['properties'][name] = self._convert_formfield(
                name=name,
                field=field
            )

    def __call__(self):
        return self.json_schema

    def _convert_formfield(self, name=None, field=None):
        widget = field.widget
        target_def = {
            'title': field.label.text,
            'description': field.description
        }

        self.path.append(name)

        if field.flags.required:
            target_def['required'] = True
            self.json_schema.setdefault('required', list())
            self.json_schema['required'].append(name)

        ftype = type(field).__name__
        methodname = '_convert_{0}'.format(ftype)
        method = getattr(self, methodname, None)

        if callable(method):
            return method(
                name=name,
                field=field
            )

        params = self.conversions.get(ftype)

        if params is not None:
            target_def.update(params)

        elif ftype == 'FormField':
            key = id(field.form_class)

            if key in self.forms_seen:
                return {'$ref': '#'.format('/'.join(self.forms_seen[key]))}

            self.forms_seen[key] = self.path
            schemagen = WTFormToJSONSchema(
                field.form_class(obj=getattr(field, '_obj', None))
            )

            target_def.update(schemagen())

        elif ftype == 'FieldList':
            if not self.include_array_title:
                target_def.pop('title')
                target_def.pop('description')

            target_def['type'] = 'array'

            subfield = field.unbound_field.bind(
                getattr(field, '_obj', None),
                name
            )

            target_def['items'] = self.convert_formfield(
                name=name,
                field=subfield
            )

            if not self.include_array_item_titles:
                target_def['items'].pop('title', None)
                target_def['items'].pop('description', None)

        else:
            try:
                input_type = widget.input_type

            except AttributeError:
                target_def['type'] = 'string'

            else:
                it = self.INPUT_TYPE_MAP.get(input_type, 'StringField')

                methodname = '_convert_{0}'.format(it)
                method = getattr(self, methodname, None)

                if callable(method):
                    return method(
                        name=name,
                        field=field
                    )

                target_def.update(self.conversions[it])

        return target_def

    def _convert_SelectField(self, field=None, **_):
        values = list()

        for val, label in field.choices:
            if isinstance(label, (list, tuple)):  # wonky option groups
                values.extend([x for x, y in label])

            else:
                values.append(val)

        target_def = {
            'title': field.label.text,
            'description': field.description,
            'enum': values,
            'ux-widget-choices': list(field.choices)
        }

        if field.flags.required:
            target_def['required'] = True

        return target_def

    def _convert_RadioField(self, field=None, **_):
        target_def = {
            'title': field.label.text,
            'description': field.description,
            'enum': [x for x, y in field.choices],
            'ux-widget': 'radio',
            'ux-widget-choices': list(field.choices)
        }

        if field.flags.required:
            target_def['required'] = True

        return target_def


def form_to_jsonschema(*args, **kwargs):
    generator = WTFormToJSONSchema(*args, **kwargs)
    return generator()
