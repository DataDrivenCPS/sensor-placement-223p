from buildingmotif import BuildingMOTIF
from buildingmotif.model_builder import TemplateBuilderContext
from buildingmotif.dataclasses import Library, Model
from buildingmotif.namespaces import bind_prefixes
from rdflib import Namespace
from utils import write_to_file

# setup our buildingmotif instance
bm = BuildingMOTIF("sqlite://")

# create the model w/ a namespace
BLDG = Namespace("urn:nrel_example/")
bldg = Model.create(BLDG)
bind_prefixes(bldg.graph)
bldg.graph.bind("bldg", BLDG)

nrel = Library.load(directory="BuildingMOTIF/libraries/ashrae/223p/nrel-templates")
water = Library.load(directory="water-templates")
s223 = Library.load(ontology_graph="BuildingMOTIF/libraries/ashrae/223p/ontology/223p.ttl")


def pipe(from_cp, to_cp):
    pipe = ctx["pipe"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp


ctx = TemplateBuilderContext(BLDG)
ctx.add_templates_from_library(nrel)
ctx.add_templates_from_library(water)

aerobic = ctx["aerobic-process-unit"](name="AEROBIC")
settler = ctx["settler"](name="SETTLER")

# connect aerobic to settler
pipe(aerobic["water-out"], settler["water-in"])

# settler sludge return goes to a junction
# make the junction
sludge_junction = ctx["junction-1to2"](name="SLUDGE_JUNCTION")

# connect the input to the junction to the sludge return of the settler with a pipe
pipe(settler["sludge-return"], sludge_junction["in1"])
# don't forget we need to connect one of the outputs of the sludge jucntion back to
# the input of the aerobic process! We'll do this in a moment

aerobic_junction = ctx["junction-2to1"](name="AEROBIC_JUNCTION")

# aerobic junction connects to input of aerobic process
pipe(aerobic_junction["out1"], aerobic["water-in"])

# pipe from settler junction to the aerobic
pipe(sludge_junction["out1"], aerobic_junction["in2"])

bldg.add_graph(ctx.compile())
graph = bldg.compile([s223.get_shape_collection()])
graph.serialize("models/kv1.ttl", format="turtle")
write_to_file(graph, "models/kv1.png")
