# -*- coding: utf-8 -*-

from knowledgebase.utils.api import (
    initialize_api,
    register_api,
    register_api_method,
    API
)
from knowledgebase.forms.vertex import VertexForm
from knowledgebase.forms.edge import EdgeForm
from knowledgebase.forms.walk import WalkForm

from flask import Blueprint, request, current_app


blueprint = initialize_api(Blueprint('graph-api', __name__))


class GraphAPI(API):
    def __init__(self, *args, **kwargs):
        super(GraphAPI, self).__init__(*args, **kwargs)

        self.graph = current_app.config['get_database']()


@register_api(
    blueprint,
    'graph-api-edge',
    '/edge',
    pk='eid',
    pk_type='string'
)
class EdgeAPI(GraphAPI):
    @register_api_method(rel='instances')
    @register_api_method(rel='instance', pk=True)
    def get(self, eid):
        if eid is None:
            return {
                'success': True,
                'data': [
                    edge.data()
                    for edge in self.graph.edges.find(**request.args)
                ]
            }, 200

        else:
            edge = self.graph.edges.get(eid)

            if edge is not None:
                return {
                    'success': True,
                    'data': edge.data()
                }, 200

            else:
                return {
                    'success': False,
                    'data': None
                }, 404

    @register_api_method(rel='create', schema=EdgeForm)
    def post(self):
        form = EdgeForm(request.form)

        if form.validate():
            source = self.graph.vertices.get(form.source.data)
            target = self.graph.vertices.get(form.target.data)

            if source is None or target is None:
                return {
                    'success': False,
                    'data': None,
                    'reason': {
                        'source': source is not None,
                        'target': target is not None
                    }
                }, 400

            properties = {
                propname: request.form[propname]
                for propname in request.form
                if propname not in ['source', 'target', 'type', 'name', 'eid']
            }

            edge = self.graph.edges.create(
                source=source.eid,
                target=target.eid,
                type=form.type.data,
                name=form.name.data,
                **properties
            )
            edge.save()

            return {
                'success': True,
                'data': edge.data()
            }, 201

        else:
            return {
                'success': False,
                'data': None,
                'reason': form.errors
            }, 400

    @register_api_method(rel='update', pk=True, schema=EdgeForm)
    def put(self, eid):
        form = EdgeForm(request.form)

        if form.validate():
            source = self.graph.vertices.get(form.source.data)
            target = self.graph.vertices.get(form.target.data)

            if source is None or target is None:
                return {
                    'success': False,
                    'data': None,
                    'reason': {
                        'source': source is not None,
                        'target': target is not None
                    }
                }, 400

            edge = self.graph.edges.get(eid)

            if edge is None:
                return {
                    'success': False,
                    'data': None
                }, 404

            edge.source = source.eid
            edge.target = target.eid
            edge.type = form.type.data
            edge.name = form.name.data

            for propname in request.form:
                if propname not in ['source', 'target', 'type', 'name', 'eid']:
                    setattr(edge, propname, request.form[propname])

            edge.save()

            return {
                'success': True,
                'data': edge.data()
            }, 200

        else:
            return {
                'success': False,
                'data': None,
                'reason': form.errors
            }, 400

    @register_api_method(rel='remove', pk=True)
    def delete(self, eid):
        self.graph.edges.delete(eid)

        return {
            'success': True,
            'data': None
        }, 200


@register_api(
    blueprint,
    'graph-api-vertex',
    '/vertex',
    pk='vid',
    pk_type='string'
)
class VertexAPI(GraphAPI):
    @register_api_method(rel='instances')
    @register_api_method(rel='instance', pk=True)
    def get(self, vid):
        if vid is None:
            return {
                'success': True,
                'data': [
                    vertex.data()
                    for vertex in self.graph.vertices.find(**request.args)
                ]
            }, 200

        else:
            vertex = self.graph.vertices.get(vid)

            if vertex is not None:
                return {
                    'success': True,
                    'data': vertex.data()
                }, 200

            else:
                return {
                    'success': False,
                    'data': None
                }, 404

    @register_api_method(rel='create', schema=VertexForm)
    def post(self):
        form = VertexForm(request.form)

        if form.validate():
            properties = {
                propname: request.form[propname]
                for propname in request.form
                if propname not in ['type', 'name', 'vid']
            }

            vertex = self.graph.vertices.create(
                type=form.type.data,
                name=form.name.data,
                **properties
            )
            vertex.save()

            return {
                'success': True,
                'data': vertex.data()
            }, 201

        else:
            return {
                'success': False,
                'data': None,
                'reason': form.errors
            }, 400

    @register_api_method(rel='update', pk=True, schema=VertexForm)
    def put(self, vid):
        form = VertexForm(request.form)

        if form.validate():
            vertex = self.graph.vertices.get(vid)

            if vertex is None:
                return {
                    'success': False,
                    'data': None
                }, 404

            vertex.type = form.type.data
            vertex.name = form.name.data

            for propname in request.form:
                if propname not in ['type', 'name', 'vid']:
                    setattr(vertex, propname, request.form[propname])

            vertex.save()

            return {
                'success': True,
                'data': vertex.data()
            }, 200

        else:
            return {
                'success': False,
                'data': None,
                'reason': form.errors
            }, 400

    @register_api_method(rel='remove', pk=True)
    def delete(self, vid):
        self.graph.vertices.delete(vid)

        return {
            'success': True,
            'data': None
        }, 200


@register_api(
    blueprint,
    'graph-api-walk',
    '/walk',
    pk='eid',
    pk_type='string'
)
class WalkAPI(GraphAPI):
    @register_api_method(rel='instances', pk=True, schema=WalkForm)
    def get(self, eid):
        if eid is None:
            return {
                'success': False,
                'data': None
            }, 501

        else:
            form = WalkForm(request.args)

            if form.validate():
                depth = form.depth.data
                lookup = form.lookup.data
                match = {
                    propname: request.args[propname]
                    for propname in request.args
                    if propname not in ['depth', 'lookup']
                }

                root_vertex = self.graph.vertices.get(eid)

                if root_vertex is None:
                    return {
                        'success': False,
                        'data': None
                    }, 404

                result = {
                    'vertices': [root_vertex],
                    'edges': []
                }

                def walk(root, iteration):
                    if iteration == 0:
                        return

                    for edge in root.outE(**match):
                        if lookup in [form.LOOKUP_EDGES, form.LOOKUP_BOTH]:
                            result['edges'].append(edge)

                        vertex = edge.outV()

                        if lookup in [form.LOOKUP_VERTICES, form.LOOKUP_BOTH]:
                            result['vertices'].append(vertex)

                        walk(vertex, iteration - 1)

                walk(root_vertex, depth)

                return {
                    'success': True,
                    'data': result
                }, 200

            else:
                return {
                    'success': False,
                    'data': None,
                    'reason': form.errors
                }, 400
