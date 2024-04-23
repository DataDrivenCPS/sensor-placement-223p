from rdflib.extras.external_graph_libs import rdflib_to_networkx_digraph
import re
from networkx import DiGraph
import rdflib
from networkx.drawing.nx_pydot import to_pydot


def with_fixed_names(graph):
    for (s, p, o) in graph:
        yield (s.replace(':','_'), p.replace(':', '_'), o.replace(':', '_'))


def write_to_file(graph: rdflib.Graph, filename: str):

    q = """SELECT ?from ?to ?edge ?fromtype ?totype WHERE {
        ?from rdf:type ?fromtype .
        ?to rdf:type ?totype .
        ?from ?edge ?to .
    }"""
    G = DiGraph()
    for (from_, to, edge, fromtype, totype) in graph.query(q):
        print(from_, to, edge, fromtype, totype)
        from_ = re.split(r'[/:#]', str(from_))[-1]
        to = re.split(r'[/:#]', str(to))[-1]
        edge = re.split(r'[/:#]', str(edge))[-1]
        fromtype = re.split(r'[/:#]', str(fromtype))[-1]
        totype = re.split(r'[/:#]', str(totype))[-1]
        G.add_node(from_, type=fromtype, label=f"{from_}\n{fromtype}")
        G.add_node(to, type=totype, label=f"{to}\n{totype}")
        G.add_edge(from_, to, type=edge)

    # convert the graph to a networkx digraph. For each node with an rdf:type edge,
    pydot_graph = to_pydot(G)
    
    # write graph to png using 'label' attribute as the node label
    pydot_graph.write_png(filename, prog='dot')
