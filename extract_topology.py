from rdflib import Namespace
import rdflib
import subprocess
import networkx as nx
from dataclasses import dataclass
from buildingmotif import BuildingMOTIF
from buildingmotif.dataclasses import Library, Model
from networkx.drawing.nx_pydot import to_pydot
import matplotlib.pyplot as plt

@dataclass
class Rule():
    query: str
    from_var: str = "from"
    edge_var: str = "conn"
    to_var: str = "to"

    def insert_nx(self, dst_graph: nx.DiGraph, src_graph: rdflib.Graph):
        result = src_graph.query(self.query)
        for row in result:
            print(f"{row=}")
            from_var = row[self.from_var].split("/")[-1]
            to_var = row[self.to_var].split("/")[-1]
            edge_var = row[self.edge_var].split("/")[-1] if row[self.edge_var] else "hasConnectionPoint"

            # 'from' is the connection point for unconnected_point. If it is an InletConnectionPoint,
            # then it is the 'from' of the edge. If it is an OutletConnectionPoint, then it is the 'to' of the edge.
            if (row[self.from_var], rdflib.RDF.type, rdflib.URIRef("http://data.ashrae.org/standard223#OutletConnectionPoint")) in src_graph:
                from_var, to_var = to_var, from_var
            dst_graph.add_edge(from_var, to_var, label=edge_var)


# default case where two things are connected via a connection
pipe = Rule(
    query="""
    PREFIX s223: <http://data.ashrae.org/standard223#>
    SELECT ?from ?conn ?to WHERE {
        ?conn s223:connectsFrom ?from .
        ?conn s223:connectsTo ?to .
    }""",
)

# might have a connection point with no connection
# in this case the "thing" points to the connection point
# we invent a new edge to represent this, called "hasConnectionPoint"
unconnected_point = Rule(
    query="""
    PREFIX s223: <http://data.ashrae.org/standard223#>
    SELECT ?from ?conn ?to WHERE {
        ?to s223:hasConnectionPoint ?from .
        FILTER NOT EXISTS {
            ?from s223:connectsThrough ?conn
        }
    }""",
)

G = nx.DiGraph()

bm = BuildingMOTIF("sqlite://", shacl_engine="topquadrant")
s223 = Library.load(ontology_graph="223p.ttl")

BLDG = Namespace("urn:nrel_example/")
bldg = Model.create(BLDG)
bldg.graph.bind("bldg", BLDG)
bldg.graph.parse("models/kv1.ttl") # change to kv1.ttl, kv2.ttl

bldg.graph.serialize("output.ttl")
pipe.insert_nx(G, bldg.graph)
unconnected_point.insert_nx(G, bldg.graph)
#unconnected_to.insert_nx(G, bldg.graph.query(unconnected_to.query))

print(G.edges(data=True))

# clean all nodes/edges from the pydot graph to only have [a-zA-Z0-9_] characters.
# change all spaces / # to underscores
G = nx.relabel_nodes(G, {node: node.replace(" ", "_").replace("#", "_") for node in G.nodes()})
# relabel edges too

# draw networkx graph in png with force-directed layout
plt.figure(figsize=(12, 12))
pydot_graph = to_pydot(G)
pydot_graph.write_png('output.png', prog='dot')
