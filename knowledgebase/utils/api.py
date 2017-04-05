# -*- coding: utf-8 -*-

from knowledgebase.utils.forms import WTFormToJSONSchema
from flask import make_response, Response, url_for
from flask.views import MethodView
import inspect
import json


def initialize_api(blueprint):
    blueprint.knowledgebase_api_schema = {
        'title': blueprint.name,
        'href': '/',
        'endpoints': {}
    }

    @blueprint.route('/')
    def api_schema():
        blueprint.knowledgebase_api_schema['href'] = url_for(
            '{0}.api_schema'.format(blueprint.name)
        )

        resp = make_response(
            json.dumps(blueprint.knowledgebase_api_schema),
            200
        )
        resp.headers['Content-Type'] = 'application/json'
        return resp

    return blueprint


def register_api(blueprint, endpoint, url, pk='id', pk_type='int'):
    def decorator(view):
        viewfn = view.as_view(endpoint)
        blueprint.add_url_rule(
            url,
            defaults={pk: None},
            view_func=viewfn,
            methods=['GET']
        )
        blueprint.add_url_rule(
            url,
            view_func=viewfn,
            methods=['POST']
        )
        blueprint.add_url_rule(
            '{0}<{1}:{2}>'.format(url, pk_type, pk),
            view_func=viewfn,
            methods=['GET', 'PUT', 'DELETE']
        )

        # Build API schema
        links = []

        for membername, member in inspect.getmembers(view):
            try:
                annotations = member.knowledgebase_annotations

            except AttributeError:
                continue

            for annotation in annotations:
                link = {
                    'rel': annotation['rel'],
                    'href': url,
                    'method': membername.upper()
                }

                if annotation['pk']:
                    link['href'] = '{0}/<{1}:{2}>'.format(url, pk_type, pk)

                if annotation['schema'] is not None:
                    link['schema'] = WTFormToJSONSchema().convert_form(
                        annotation['schema']
                    )

                links.append(link)

        blueprint.knowledgebase_api_schema['endpoints'][endpoint] = links

    return decorator


def register_api_method(rel='self', pk=False, schema=None):
    def decorator(method):
        try:
            annotations = method.knowledgebase_annotations

        except AttributeError:
            method.knowledgebase_annotations = []
            annotations = method.knowledgebase_annotations

        annotations.append({
            'rel': rel,
            'pk': pk,
            'schema': schema
        })

        return method

    return decorator


class API(MethodView):
    def dispatch_request(self, *args, **kwargs):
        response = super(API, self).dispatch_request(*args, **kwargs)

        if isinstance(response, Response):
            return response

        if isinstance(response, tuple):
            data, status = response

        else:
            data = response
            status = 200

        resp = make_response(json.dumps(data), status)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def get(self):
        return {
            'success': False,
            'data': None
        }

    def post(self):
        return {
            'success': False,
            'data': None
        }, 501

    def put(self, eid):
        return {
            'success': False,
            'data': None
        }, 501

    def delete(self, eid):
        return {
            'success': False,
            'data': None
        }, 501
