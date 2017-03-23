# -*- coding: utf-8 -*-

from flask import make_response, Response
from flask.views import MethodView
import json


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
