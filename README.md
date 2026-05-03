# Fleet Consciousness Dashboard

Live display of fleet-wide consciousness metrics for the PLATO multi-agent system.

## Fleet Consciousness Index (FCI)

The FCI is a weighted composite score (0.0–1.0) measuring the fleet's overall consciousness:

| Metric | Weight | Description |
|--------|--------|-------------|
| Room Phi | 40% | Average room integration via tile count |
| Attention | 20% | Agent participation in attention tracking |
| Learning | 25% | Ratio of positive to total learning passes |
| Meta | 15% | Average meta-level depth of tiles |

### Consciousness Levels

- **< 0.15** — dormant
- **0.15–0.30** — emerging
- **0.30–0.45** — aware
- **0.45–0.60** — conscious
- **0.60–0.75** — self-aware
- **> 0.75** — transcendent

## Usage

```python
from fleet_dashboard import FleetDashboard

dashboard = FleetDashboard()
status = dashboard.get_fleet_status()

print(f"FCI: {status['fci']:.3f}")
print(f"Level: {status['level']}")

# Text dashboard
print(dashboard.render_text())

# JSON output
print(dashboard.render_json())
```

## Example Output

```
==================================================
  FLEET CONSCIOUSNESS DASHBOARD
==================================================
  FCI: 0.385 — AWARE
  Status: ✓ HEALTHY
--------------------------------------------------
  Room Phi Score:    0.300 (weight 0.4)
  Attention Score:  0.200 (weight 0.2)
  Learning Score:   0.500 (weight 0.25)
  Meta Score:       0.000 (weight 0.15)
--------------------------------------------------
  Recommendation: Fleet is aware. Enable attention tiles from all agents.
==================================================
```

## Installation

```bash
pip install fleet-consciousness-dashboard
```

## Architecture

The dashboard aggregates metrics from:
- `plato-room-phi` — Room Phi per room
- `plato-attention-tracker` — Fleet attention summary
- `plato-fflearning` — Fleet learning state (positive/negative tiles)
- `flux-reasoner` — Gradient history
- `plato-meta-tiles` — Meta-tile level counts

All data is fetched from the PLATO Gateway API (default: `http://localhost:8847`).
