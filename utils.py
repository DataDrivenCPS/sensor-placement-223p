from rdflib.extras.external_graph_libs import rdflib_to_networkx_digraph
import rdflib
from networkx.drawing.nx_pydot import to_pydot


def with_fixed_names(graph):
    for (s, p, o) in graph:
        yield (s.replace(':','_'), p.replace(':', '_'), o.replace(':', '_'))


def write_to_file(graph: rdflib.Graph, filename: str):
    g = rdflib_to_networkx_digraph(with_fixed_names(graph))

    pydot_graph = to_pydot(g)
    pydot_graph.write_png(filename)
