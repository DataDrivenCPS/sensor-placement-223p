from buildingmotif import BuildingMOTIF
from buildingmotif.dataclasses import Library

# setup our buildingmotif instance
bm = BuildingMOTIF("sqlite://", shacl_engine="topquadrant")

nrel = Library.load(directory="BuildingMOTIF/libraries/ashrae/223p/nrel-templates")
water = Library.load(directory="water-templates")
#s223 = Library.load(ontology_graph="223p.ttl")

for template in water.get_templates():
    inlined = template.inline_dependencies()
    print(template.name, len(inlined.body))
