from buildingmotif import BuildingMOTIF
from buildingmotif.model_builder import TemplateBuilderContext
from buildingmotif.dataclasses import Library, Model
from buildingmotif.namespaces import bind_prefixes
from rdflib import Namespace
from utils import write_to_file

# setup our buildingmotif instance
bm = BuildingMOTIF("sqlite://", shacl_engine="topquadrant")

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
anoxic = ctx["anoxic"](name="ANOXIC")

# input junction
input_junction = ctx["junction-2to1"](name="INPUT")

# carbon dosing junction
carbon_junction = ctx["carbon-dosing-junction"](name="CARBON")

# input to carbon
pipe(input_junction["out1"], carbon_junction["water-in"])

# carbon to anoxic
pipe(carbon_junction["water-out"], anoxic["water-in"])

# anoxic to aerobic
pipe(anoxic["water-out"], aerobic["water-in"])
# aerobic to settler
pipe(aerobic["water-out"], settler["water-in"])

# settler return junction
settler_junction = ctx["junction-1to2"](name="SETTLER_RETURN")
pipe(settler["sludge-return"], settler_junction["in1"])
pipe(settler_junction["out1"], input_junction["in2"])

# aerobic recycle
pipe(aerobic["aerobic-recycle"], anoxic["aerobic-recycle"])

bldg.add_graph(ctx.compile())
graph = bldg.compile([s223.get_shape_collection()])
graph.serialize("models/kv2.ttl", format="turtle")
write_to_file(graph, "models/kv2.png")
