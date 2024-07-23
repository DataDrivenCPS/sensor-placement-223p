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

def pipe_chemical(from_cp, to_cp):
    pipe = ctx["pipe-chemical"]
    pipe["a"] = from_cp
    pipe["b"] = to_cp

ctx = TemplateBuilderContext(BLDG)
ctx.add_templates_from_library(nrel)
ctx.add_templates_from_library(water)

ocean = ctx["ocean"](name="OCEAN")

# PRETREATMENT
intake = ctx["intake"](name="INTAKE")

ferric_chloride_tank = ctx["chemical-tank"](name="FECL3_TANK")
ferric_chloride_pump = ctx["dosing-pump"](name="FECL3_PUMP")
ferric_chloride = ctx["dosing-point"](name="FECL3_DOSING_POINT")

chlorination_tank = ctx["chemical-tank"](name="CHLORINE_TANK")
chlorination_pump = ctx["dosing-pump"](name="CHLORINE_PUMP")
chlorination_point =    ctx["dosing-point"](name="CHLORINE_DOSING_POINT")
chlorination_basin = ctx["chlorination-basin"](name="CHLORINATION-BASIN")

static_mixer = ctx["static-mixer"](name="STATIC_MIXER")
storage_tank_1 = ctx["storage-tank"](name="STORAGE_TANK_1")
media_filtration = ctx["media-filter"](name="MEDIA_FILTER")

backwash_pump = ctx["backwash-pump"](name="BACKWASH_PUMP")
backwash_thickener = ctx["backwash-thickener"](name="BACKWASH_THICKENER")
dumpster = ctx["dumpster"](name="DUMPSTER")

anti_scalant_tank = ctx["chemical-tank"](name="ANTI_SCALANT_TANK")
anti_scalant_pump = ctx["dosing-pump"](name="ANTI_SCALANT_PUMP")
anti_scalant = ctx["dosing-point"](name="ANTI_SCALANT_DOSING_POINT")

cartridge_filtration = ctx["cartridge-filter"](name="CARTRIDGE_FILTER")

# DESAL PRESSURE EXCHANGER
separator = ctx["separator"](name="SEPARATOR")
pump1_1 = ctx["pump"](name="PUMP1.1")
pump1_2 = ctx["pump"](name="PUMP1.2")
mixer = ctx["mixer2"](name="MIXER")
pressure_exchanger = ctx["pressure-exchanger"](name="PRESSURE_EXCHANGER")
reverse_osmosis1 = ctx["reverse-osmosis"](name="REVERSE_OSMOSIS1")
disposal = ctx["disposal"](name="DISPOSAL")

# POST TREATMENT
storage_tank_2 = ctx["storage-tank"](name="STORAGE_TANK_2")
ozone_generator = ctx["ozone-generator"](name="OZONE_GENERATOR")
ozone_pump = ctx["dosing-pump"](name="OZONE_PUMP")
ozone_dosing_point = ctx["dosing-point"](name="OZONE_DOSING_POINT")
uvaop = ctx["UV-Reactor"](name="UV-AOP-Reactor")

CO2_canister = ctx["CO2-canister"](name="CO2_CANISTER")
CO2_pump = ctx["dosing-pump"](name="CO2_PUMP")
CO2_addition = ctx["dosing-point"](name="CO2_DOSING_POINT")

lime_tank = ctx["chemical-tank"](name="LIME_TANK")
lime_pump = ctx["dosing-pump"](name="LIME_PUMP")
lime_addition = ctx["dosing-point"](name="LIME_DOSING_POINT")

storage_tank3 = ctx["storage-tank"](name="STORAGE_TANK_3")

municipal_water = ctx["municipal-water"](name="MUNICIPAL_WATER")

# PIPES:
### PRETREATMENT
pipe_water(ocean["water-out"], intake["water-in"])
pipe_water(intake["water-out"], ferric_chloride["water-in"])
pipe_chemical(ferric_chloride_tank["chemical-out"], ferric_chloride_pump["chemical-in"])
pipe_chemical(ferric_chloride_pump["chemical-out"], ferric_chloride["chemical-in"])
pipe_water(ferric_chloride["water-out"], chlorination_point["water-in"])
pipe_chemical(chlorination_tank["chemical-out"], chlorination_pump["chemical-in"])
pipe_chemical(chlorination_pump["chemical-out"], chlorination_point["chemical-in"])
pipe_water(chlorination_point["water-out"], chlorination_basin["water-in"])
pipe_water(chlorination_basin["water-out"], static_mixer["water-in"])
pipe_water(static_mixer["water-out"], storage_tank_1["water-in"])
pipe_water(storage_tank_1["water-out"], media_filtration["water-in"])
pipe_water(media_filtration["water-out"], anti_scalant["water-in"])
pipe_chemical(anti_scalant_tank["chemical-out"], anti_scalant_pump["chemical-in"])
pipe_chemical(anti_scalant_pump["chemical-out"], anti_scalant["chemical-in"])

pipe_waste(media_filtration["waste-out"], backwash_pump["waste-in"])
pipe_waste(backwash_pump["waste-out"], backwash_thickener["waste-in"])
pipe_waste(backwash_thickener["waste-out"], dumpster["waste-in"])

pipe_water(anti_scalant["water-out"], cartridge_filtration["water-in"])
pipe_water(cartridge_filtration["water-out"], separator["water-in"])

### DESAL PRESSURE EXCHANGER

pipe_water(separator["water-out1"], pump1_1["water-in"])
pipe_water(separator["water-out2"], pressure_exchanger["water-in1"])
pipe_water(pump1_1["water-out"], mixer["water-in1"])
pipe_water(pressure_exchanger["water-out1"], pump1_2["water-in"])
pipe_waste(pressure_exchanger["waste-out"], disposal["waste-in1"])
pipe_waste(disposal['waste-out'],ocean["waste-in"])
pipe_water(pump1_2["water-out"], mixer["water-in2"])
pipe_water(mixer["water-out"], reverse_osmosis1["water-in"]) 
pipe_waste(reverse_osmosis1["waste-out"], pressure_exchanger["waste-in"])
pipe_water(reverse_osmosis1["water-out"],  storage_tank_2["water-in"])

### POST TREATMENT
pipe_water(storage_tank_2["water-out"], ozone_dosing_point["water-in"])
pipe_water(ozone_dosing_point["water-out"], uvaop["water-in"])
pipe_chemical(ozone_generator["chemical-out"], ozone_pump["chemical-in"])
pipe_chemical(ozone_pump["chemical-out"], ozone_dosing_point["chemical-in"])
pipe_water(uvaop["water-out"], CO2_addition["water-in"])
pipe_chemical(CO2_canister["chemical-out"], CO2_pump["chemical-in"])
pipe_chemical(CO2_pump["chemical-out"], CO2_addition["chemical-in"])
pipe_water(CO2_addition["water-out"], lime_addition["water-in"])
pipe_chemical(lime_tank["chemical-out"], lime_pump["chemical-in"])
pipe_chemical(lime_pump["chemical-out"], lime_addition["chemical-in"])

pipe_water(lime_addition["water-out"], storage_tank3["water-in"])
pipe_water(storage_tank3["water-out"], municipal_water["water-in"])

bldg.add_graph(ctx.compile())
graph = bldg.compile([s223.get_shape_collection()])
graph.serialize("models/desal.ttl", format="turtle")
write_to_file(graph, "models/desal.png")
