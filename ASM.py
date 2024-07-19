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
water = Library.load(directory="water-templates-2")
s223 = Library.load(ontology_graph="223p.ttl")


def pipe(from_cp, to_cp):
    pipe = ctx["pipe"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp


ctx = TemplateBuilderContext(BLDG)
ctx.add_templates_from_library(nrel)
ctx.add_templates_from_library(water)

# input junction
input_junction = ctx["junction-3to1"](name="INPUT")

anoxic1 = ctx["anoxic2"](name="ANOXIC_TANK_1")

anoxic2 = ctx["anoxic2"](name="ANOXIC_TANK_2")

aerobic1 = ctx["aerobic-process-unit2"](name="AEROBIC_TANK_1")
aerobic2 = ctx["aerobic-process-unit2"](name="AEROBIC_TANK_2")
aerobic3 = ctx["aerobic-process-unit2"](name="AEROBIC_TANK_3")

aero_junction = ctx["junction-1to2"](name="AEROBIC_JUNCTION")

clarifier = ctx["clarifier"](name="SEC_CLARIFIER")

sludge_junction = ctx["junction-1to2"](name="SLUDGE_JUNCTION")

# input to anoxic
pipe(input_junction["out1"], anoxic1["water-in"])

# anoxic to anoxic
pipe(anoxic1["water-out"], anoxic2["water-in"])

# anoxic to aerobic
pipe(anoxic2["water-out"], aerobic1["water-in"])

#aerobic to aerobic
pipe(aerobic1["water-out"], aerobic2["water-in"])
pipe(aerobic2["water-out"], aerobic3["water-in"])

# aerobic to settler
pipe(aerobic3["water-out"], aero_junction["in1"])

# aerobic junction to input junction
pipe(aero_junction["out1"], input_junction["in2"])

# aerobic junction to clarifier
pipe(aero_junction["out2"], clarifier["water-in"])

# clarifier to sludge junction
pipe(clarifier["sludge-return"], sludge_junction["in1"])

# sludge junction to input junction
pipe(sludge_junction["out1"], input_junction["in3"])

bldg.add_graph(ctx.compile())
graph = bldg.compile([s223.get_shape_collection()])
graph.serialize("models/asm.ttl", format="turtle")
write_to_file(graph, "models/asm.png")
