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
poetry run python kv-system-1.py
poetry run python kv-system-2.py
```
