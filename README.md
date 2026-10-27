# EcoSorb Pods — open-source proof of concept

EcoSorb Pods is a **proposed** AI-assisted, multi-pod marine oil-spill cleanup system. The accompanying handbook describes a workflow from Sentinel-1 SAR imagery through Google Earth Engine (GEE), zone allocation, GPS coverage waypoints, and floating pods using replaceable kapok-fiber absorbents. This repository implements a **small offline planning and fleet simulation demonstrator**, not a production, physically validated oil recovery platform.

## What's implemented
- Reads an **example spill polygon** in local metric coordinates from JSON (not real satellite-derived data).
- Estimates spill area and a rough oil mass from user-supplied thickness and oil density.
- Estimates cartridge/pod mission loads and partitions a rectangular demo area into strips.
- Generates lawnmower-style local waypoints per strip.
- Simulates pod missions and telemetry transitions including return on low battery or full cartridge.
- Python unit tests; example inputs and generated mission output.

## Not yet implemented
Actual Sentinel-1/GEE spill classification; robust arbitrary-polygon geospatial operations; real AI/ML training; real GPS route following; ESP32 firmware and LoRa driver integration; collision avoidance, field safety certification, oil absorption testing, and ocean deployment. See [roadmap](docs/ROADMAP.md).

## Quick start
Requires **Python 3.10+**, with no third-party packages for this offline demonstrator.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
python -m ecosorb.cli --input data/sample_spill.json --output output/mission.json
python -m unittest discover -s tests -v
```

## Configuration / environment variables
The demo requires **no secrets or environment variables**. All inputs are in `data/sample_spill.json`. Future cloud integration could require `GOOGLE_CLOUD_PROJECT` and Google Earth Engine credentials, **but these are not supported by this implementation**. Never commit credentials.

## Input data
Coordinates are **local meters**, not latitude/longitude. For planning only, sample spill is an axis-aligned rectangle. `oil_thickness_m` is an illustrative assumption, not satellite-measured thickness; `oil_density_kg_m3` and `cartridge_capacity_kg` are assumed demo inputs, not laboratory results.

## Key concepts
`estimated_mass_kg = area_m2 × thickness_m × density_kg_m3`;
`required_cartridge_loads = ceil(estimated_mass_kg / cartridge_capacity_kg)`.
Loads are **cartridge-equivalents**, not necessarily the simultaneous pod fleet size: pods may be redeployed. Example chooses `available_pods` and allocates equal strip zones to those pods. Actual cleaning throughput depends on verified absorption and conditions.

## Structure
- `ecosorb/` — standalone Python planning and mock pod telemetry
- `data/` — fictional representative example, **not observed spill data**
- `tests/` — reproducible unit tests
- `docs/TECHNICAL_DESIGN.md` — architecture and data flow diagrams
- `docs/ROADMAP.md` — limitations and validation needs
- `LICENSE` — MIT License

## Safety and project status
**Do not deploy this code to physical equipment or at an actual spill.** Autonomous navigation needs safety engineering, geofencing, human supervision, regulations, marine testing, and environmental evaluation. The project handbook is a design source, not evidence that the full system has been built or validated.
