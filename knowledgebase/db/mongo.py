# -*- coding: utf-8 -*-

from knowledgebase.db.base import Vertex as BaseVertex
from knowledgebase.db.base import Edge as BaseEdge
from knowledgebase.db.base import ElementView as BaseElementView
from knowledgebase.db.base import Graph as BaseGraph

from bson.objectid import ObjectId
from pymongo import MongoClient
from copy import deepcopy


VERTEX_COLLECTION = 'kb_vertices'
EDGE_COLLECTION = 'kb_edges'


class Vertex(BaseVertex):
    __collection__ = VERTEX_COLLECTION

    @classmethod
    def get(cls, graph, eid):
        elt = graph.db[VERTEX_COLLECTION].find_one({'_id': ObjectId(eid)})

        if elt is not None:
            elt['eid'] = str(elt.pop('_id'))
            elt = cls(graph, data=elt)

        return elt

    @classmethod
    def get_all(cls, graph):
        elts = graph.db[VERTEX_COLLECTION].find()

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = cls(graph, data=elt)
            yield elt

    def save(self):
        doc = self.data()

        if self.eid is not None:
            _id = ObjectId(doc.pop('eid'))
            self._graph.db[VERTEX_COLLECTION].replace_one(
                {'_id': _id},
                doc
            )

        else:
            ret = self._graph.db[VERTEX_COLLECTION].insert_one(doc)
            self.eid = str(ret.inserted_id)

    def outE(self, **properties):
        properties['source'] = ObjectId(self.eid)
        elts = self._graph.db[EDGE_COLLECTION].find(properties)

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = self._graph.edge_class(self._graph, data=elt)
            yield elt

    def inE(self, **properties):
        properties['target'] = ObjectId(self.eid)
        elts = self._graph.db[EDGE_COLLECTION].find(properties)

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = self._graph.edge_class(self._graph, data=elt)
            yield elt

    def bothE(self, **properties):
        src_properties = deepcopy(properties)
        src_properties['source'] = ObjectId(self.eid)

        tgt_properties = deepcopy(properties)
        tgt_properties['target'] = ObjectId(self.eid)

        elts = self._graph.db[EDGE_COLLECTION].find({
            '$or': [
                src_properties,
                tgt_properties
            ]
        })

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = self._graph.edge_class(self._graph, data=elt)
            yield elt


class Edge(BaseEdge):
    __collection__ = EDGE_COLLECTION

    @classmethod
    def get(cls, graph, eid):
        elt = graph.db[EDGE_COLLECTION].find_one({'_id': ObjectId(eid)})

        if elt is not None:
            elt['eid'] = str(elt.pop('_id'))
            elt = cls(graph, data=elt)

        return elt

    @classmethod
    def get_all(cls, graph):
        elts = graph.db[EDGE_COLLECTION].find()

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = cls(graph, data=elt)
            yield elt

    def save(self):
        doc = self.data()

        if self.eid is not None:
            _id = ObjectId(doc.pop('eid'))
            self._graph.db[EDGE_COLLECTION].replace_one(
                {'_id': _id},
                doc
            )

        else:
            ret = self._graph.db[EDGE_COLLECTION].insert_one(doc)
            self.eid = str(ret.inserted_id)

    def outV(self):
        elt = self._graph.db[VERTEX_COLLECTION].find_one({
            '_id': ObjectId(self.target)
        })

        if elt is not None:
            elt['eid'] = str(elt.pop('_id'))
            elt = self._graph.vertex_class(self._graph, data=elt)

        return elt

    def inV(self):
        elt = self._graph.db[VERTEX_COLLECTION].find_one({
            '_id': ObjectId(self.source)
        })

        if elt is not None:
            elt['eid'] = str(elt.pop('_id'))
            elt = self._graph.vertex_class(self._graph, data=elt)

        return elt

    def bothV(self):
        elts = self._graph.db[VERTEX_COLLECTION].find({
            '_id': {'$in': [
                ObjectId(self.source),
                ObjectId(self.target)
            ]}
        })

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = self._graph.vertex_class(self._graph, data=elt)
            yield elt


class ElementView(BaseElementView):
    def find(self, **properties):
        elts = self.graph.db[self.cls.__collection__].find(properties)

        for elt in elts:
            elt['eid'] = str(elt.pop('_id'))
            elt = self.cls(self.graph, data=elt)
            yield elt

    def update(self, eid, **data):
        self.graph.db[self.cls.__collection__].update_one(
            {'_id': ObjectId(eid)},
            {'$set': data}
        )

    def delete(self, eid):
        self.graph.db[self.cls.__collection__].remove_one(
            {'_id': ObjectId(eid)}
        )


class Graph(BaseGraph):

    elementview_class = ElementView
    vertex_class = Vertex
    edge_class = Edge

    def __init__(self, *args, **kwargs):
        super(Graph, self).__init__(*args, **kwargs)

        self.conn = MongoClient(self.conf.uri)
        self.db = self.conn.get_default_database()

        if self.conf.username is not None and self.conf.password is not None:
            self.db.authenticate(self.conf.username, self.conf.password)
