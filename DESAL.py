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

def pipe_waste(from_cp, to_cp):
    pipe = ctx["pipe-waste"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

ctx = TemplateBuilderContext(BLDG)
ctx.add_templates_from_library(nrel)
ctx.add_templates_from_library(water)

# PRETREATMENT
feed = ctx["feed"](name="FEED")
intake = ctx["intake"](name="INTAKE")
ferric_chloride = ctx["chemical-addition"](name="FECL3_ADDITION")
chlorination = ctx["chlorination"](name="CHLORINATION")
static_mixer = ctx["static-mixer"](name="STATIC_MIXER")
storage_tank_1 = ctx["storage-tank"](name="STORAGE_TANK_1")
media_filtration = ctx["media-filtration"](name="MEDIA_FILTRATION")
anti_scalant = ctx["chemical-addition"](name="ANTI_SCALANT")
backwash = ctx["backwash-solids-handling"](name="BACKWASH")
landfill = ctx["landfill"](name="LANDFILL")
cartridge_filtration = ctx["cartridge-filtration"](name="CARTRIDGE_FILTRATION")

junction_left = ctx["junction-1to2"](name="PRETREATMENT_JUNCTION")

# DESAL PRESSURE EXCHANGER
separator = ctx["separator"](name="SEPARATOR")
pump1_1 = ctx["pump"](name="PUMP1.1")
pump1_2 = ctx["pump"](name="PUMP1.2")
mixer = ctx["mixer2"](name="MIXER")
pressure_exchanger = ctx["pressure-exchanger"](name="PRESSURE_EXCHANGER")
reverse_osmosis1 = ctx["reverse-osmosis"](name="REVERSE_OSMOSIS1")

# DESAL PUMP AS TURBINE

pump2_1 = ctx["pump"](name="PUMP2.1")
reverse_osmosis2 = ctx["reverse-osmosis"](name="REVERSE_OSMOSIS2")
energy_recovery_device = ctx["energy-recovery-device"](name="ENERGY_RECOVERY_DEVICE")


junction_right = ctx["junction-2to1"](name="DESAL_JUNCTION")
disposal = ctx["disposal"](name="DISPOSAL")

# POST TREATMENT
storage_tank_2 = ctx["storage-tank"](name="STORAGE_TANK_2")
uvaop = ctx["UV-AOP"](name="UV-AOP")
CO2_addition = ctx["CO2-addition"](name="CO2_ADDITION")
lime_addition = ctx["chemical-addition"](name="LIME_ADDITION")
storage_tank3 = ctx["storage-tank"](name="STORAGE_TANK_3")

municipal_water = ctx["municipal-water"](name="MUNICIPAL_WATER")

# PIPES:
### PRETREATMENT
pipe_water(feed["water-out"], intake["water-in"])
pipe_water(intake["water-out"], ferric_chloride["water-in"])
pipe_water(ferric_chloride["water-out"], chlorination["water-in"])
pipe_water(chlorination["water-out"], static_mixer["water-in"])
pipe_water(static_mixer["water-out"], storage_tank_1["water-in"])
pipe_water(storage_tank_1["water-out"], media_filtration["water-in"])
pipe_water(media_filtration["water-out"], anti_scalant["water-in"])
pipe_waste(media_filtration["waste-out"], backwash["waste-in"])
pipe_waste(backwash["waste-out"], landfill["waste-in"])
pipe_water(anti_scalant["water-out"], cartridge_filtration["water-in"])
pipe_water(cartridge_filtration["water-out"], junction_left["in1"])

### DESAL PRESSURE EXCHANGER

pipe_water(junction_left["out1"], separator["water-in"])
pipe_water(separator["water-out1"], pump1_1["water-in"])
pipe_water(separator["water-out2"], pressure_exchanger["water-in1"])
pipe_water(pump1_1["water-out"], mixer["water-in1"])
pipe_water(pressure_exchanger["water-out1"], pump1_2["water-in"])
pipe_waste(pressure_exchanger["waste-out"], disposal["waste-in1"])
pipe_water(pump1_2["water-out"], mixer["water-in2"])
pipe_water(mixer["water-out"], reverse_osmosis1["water-in"]) 
pipe_waste(reverse_osmosis1["waste-out"], pressure_exchanger["waste-in"])
pipe_water(reverse_osmosis1["water-out"], junction_right["in1"])

### DESAL PUMP AS TURBINE
pipe_water(junction_left["out2"], pump2_1["water-in"])
pipe_water(pump2_1["water-out"], reverse_osmosis2["water-in"])
pipe_water(reverse_osmosis2["water-out"], junction_right["in2"])
pipe_waste(reverse_osmosis2["waste-out"], energy_recovery_device["waste-in"])
pipe_waste(energy_recovery_device["waste-out"], disposal["waste-in2"])

### POST TREATMENT
pipe_water(junction_right["out1"], storage_tank_2["water-in"])
pipe_water(storage_tank_2["water-out"], uvaop["water-in"])
pipe_water(uvaop["water-out"], CO2_addition["water-in"])
pipe_water(CO2_addition["water-out"], lime_addition["water-in"])
pipe_water(lime_addition["water-out"], storage_tank3["water-in"])
pipe_water(storage_tank3["water-out"], municipal_water["water-in"])

bldg.add_graph(ctx.compile())
graph = bldg.compile([s223.get_shape_collection()])
graph.serialize("models/desal.ttl", format="turtle")
write_to_file(graph, "models/desal.png")
