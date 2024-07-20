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
s223 = Library.load(ontology_graph="223p.ttl")

def pipe_water(from_cp, to_cp):
    pipe = ctx["pipe-water"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

def pipe_biogas(from_cp, to_cp):
    pipe = ctx["pipe-biogas"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

def pipe_sludge(from_cp, to_cp):
    pipe = ctx["pipe-sludge"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

def pipe_fog(from_cp, to_cp):
    pipe = ctx["pipe-fog"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

def pipe_electricity(from_cp, to_cp):
    pipe = ctx["pipe-electricity"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

ctx = TemplateBuilderContext(BLDG)
ctx.add_templates_from_library(nrel)
ctx.add_templates_from_library(water)


bar_screen = ctx["bar-screen"](name="BAR_SCREEN")

lift_pump = ctx["lift-pump"](name="LIFT_PUMP")

grit_chamber = ctx["grit-chamber"](name="GRIT_CHAMBER")

primary_clarifier = ctx["clarifier2"](name="PRIMARY_CLARIFIER")

aeration_basin = ctx["aeration-basin"](name="AERATION_BASIN")

ras_pump = ctx["RAS-pump"](name="RAS_PUMP")

secondary_clarifier = ctx["clarifier3"](name="SECONDARY_CLARIFIER")

gravity_thickener = ctx["gravity-thickener"](name="GRAVITY_THICKENER")

contact_chamber = ctx["contact-chamber"](name="CONTACT_CHAMBER")

anaerobic_digester = ctx["anaerobic-digester"](name="ANAEROBIC_DIGESTION")

fog_tank = ctx["fog-tank"](name="FOG_TANK")

fog_pump = ctx["fog-pump"](name="FOG_PUMP")

conditioner = ctx["conditioner"](name="CONDITIONER")

flare = ctx["flare"](name="FLARE")

cogenerator  = ctx["cogenerator"](name="COGENERATOR")

virtual_demand = ctx["virtual-demand"](name="VIRTUAL_DEMAND")

battery = ctx["battery"](name="BATTERY")

pipe_water(bar_screen['untreated-sewage-out'],lift_pump['untreated-sewage-in'])
pipe_water(lift_pump['untreated-sewage-out'],grit_chamber['untreated-sewage-in'])
pipe_water(grit_chamber['untreated-sewage-out'],primary_clarifier['untreated-sewage-in'])
pipe_water(primary_clarifier['untreated-sewage-out'],aeration_basin['untreated-sewage-in'])
pipe_water(aeration_basin['untreated-sewage-out'],secondary_clarifier['untreated-sewage-in'])
pipe_water(secondary_clarifier['untreated-sewage-out'],contact_chamber['untreated-sewage-in'])

pipe_sludge(primary_clarifier['sludge-out'],gravity_thickener['sludge-in1'])
pipe_sludge(secondary_clarifier['sludge-out1'],gravity_thickener['sludge-in2'])
pipe_sludge(secondary_clarifier["sludge-out2"],ras_pump["sludge-in"])
pipe_sludge(ras_pump["sludge-out"],aeration_basin["sludge-in"])
pipe_sludge(gravity_thickener["sludge-out"],anaerobic_digester["sludge-in"])

pipe_fog(fog_tank["fog-out"],fog_pump["fog-in"])
pipe_fog(fog_pump["fog-out"],anaerobic_digester["fog-in"])

pipe_biogas(anaerobic_digester["biogas-out"],conditioner["biogas-in"])
pipe_biogas(conditioner["biogas-out1"],flare["biogas-in"])
pipe_biogas(conditioner["biogas-out2"],cogenerator["biogas-in"])

pipe_electricity(cogenerator["electricity-out"],virtual_demand["electricity-in2"])
pipe_electricity(virtual_demand["electricity-out"],battery["electricity-in"])
pipe_electricity(battery["electricity-out"],virtual_demand["electricity-in3"])

bldg.add_graph(ctx.compile())
graph = bldg.compile([s223.get_shape_collection()])
graph.serialize("models/wwtp.ttl", format="turtle")
write_to_file(graph, "models/wwtp.png")
