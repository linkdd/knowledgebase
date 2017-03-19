# -*- coding: utf-8 -*-


def register_view(blueprint, endpoint, url, pk='id', pk_type='int'):
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
            '{0}<{1}:{2}>'.format(url, pk, pk_type),
            view_func=viewfn,
            methods=['GET', 'PUT', 'DELETE']
        )
