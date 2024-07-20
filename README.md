# Sensor Placement on WWTP

Modeling a few basic waste water treatment plants with [ASHRAE 223P](https://open223.info) to experiment with doing the optimal sensor placement computation from [this paper](https://doi.org/10.1016/j.watres.2016.05.068).

Models are located in the `models/` directory

## Setup

```bash
git clone --recurse-submodules https://github.com/DataDrivenCPS/sensor-placement-223p
poetry install
```

## Create the models

```bash
mkdir -p models/
poetry run python kv-system-1.py
poetry run python kv-system-2.py
```

## Models

### Activated Sludge Model (ASM)
[ASM1](https://watertap.readthedocs.io/en/latest/technical_reference/flowsheets/ASM1.html)

[MODEL CODE](./ASM.py)

[RESULT GRAPH](./models/asm.png)

### Wastewater Treatement Plant (WWTP)
"I have a publicly available WWTP model in PyPES of a dummy system" -Fletcher

[WWTP](https://github.com/we3lab/pype-schema/blob/main/pype_schema/data/sample.json)

[MODEL CODE](WWTP.py)

[RESULT GRAPH](./models/wwtp.png)