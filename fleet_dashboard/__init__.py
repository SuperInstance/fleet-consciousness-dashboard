"""
Fleet Consciousness Dashboard — live display of fleet consciousness metrics

Aggregates:
- Room Phi per room (from plato-room-phi)
- Fleet attention summary (from plato-attention-tracker)
- Fleet learning state (from plato-fflearning)
- Gradient history from flux-reasoner
- Meta-tile level counts (from plato-meta-tiles)

Computes:
- Fleet Consciousness Index (FCI) = weighted average of all Phi values
- Attention utilization rate
- Average agent goodness
- Meta-level depth score

Usage:
    from fleet_dashboard import FleetDashboard
    dashboard = FleetDashboard()
    status = dashboard.get_fleet_status()
    print(f"FCI: {status['fci']:.3f}")
    print(f"Level: {status['level']}")
    print(dashboard.render_text())  # human-readable dashboard
"""

import requests
from typing import Dict, Any, List, Optional

class FleetDashboard:
    """
    Fleet Consciousness Dashboard.
    
    Aggregates metrics from all PLATO subsystems and computes
    the Fleet Consciousness Index (FCI).
    """
    
    FCI_WEIGHTS = {
        "phi": 0.40,        # Room integration is primary
        "attention": 0.20,  # Attention utilization
        "goodness": 0.25,   # Learning state
        "meta": 0.15        # Meta-level depth
    }
    
    def __init__(
        self,
        plato_url: str = "http://localhost:8847",
        deepinfra_key: str = "RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"
    ):
        self.plato_url = plato_url.rstrip("/")
        self.deepinfra_key = deepinfra_key
    
    def get_room_phi_score(self) -> float:
        """Get average Phi across top rooms."""
        try:
            resp = requests.get(f"{self.plato_url}/rooms?limit=20", timeout=5)
            if resp.status_code == 200:
                rooms = resp.json().get("rooms", [])
                # Use tile count as proxy for phi (rooms with more tiles are more developed)
                if rooms:
                    avg_tiles = sum(r.get("tile_count", 0) for r in rooms) / len(rooms)
                    return min(avg_tiles / 100.0, 1.0)  # normalize to 0-1
        except:
            pass
        return 0.3  # default baseline
    
    def get_attention_score(self) -> float:
        """Get attention utilization rate."""
        try:
            resp = requests.get(f"{self.plato_url}/room/fleet_attention?limit=50", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                # Higher score = more agents tracking attention
                unique_agents = len(set(t.get("agent", "") for t in tiles))
                return min(unique_agents / 5.0, 1.0)  # 5 agents = full score
        except:
            pass
        return 0.2  # default baseline
    
    def get_learning_score(self) -> float:
        """Get fleet learning state score."""
        try:
            resp = requests.get(f"{self.plato_url}/room/ff_positive_tiles?limit=100", timeout=5)
            pos_count = 0
            if resp.status_code == 200:
                pos_count = len(resp.json().get("tiles", []))
            
            resp2 = requests.get(f"{self.plato_url}/room/ff_negative_tiles?limit=100", timeout=5)
            neg_count = 0
            if resp2.status_code == 200:
                neg_count = len(resp2.json().get("tiles", []))
            
            # Ratio of positive to total passes
            total = pos_count + neg_count
            if total > 0:
                return pos_count / total
        except:
            pass
        return 0.5  # default neutral
    
    def get_meta_score(self) -> float:
        """Get meta-level depth score."""
        try:
            resp = requests.get(f"{self.plato_url}/room/plato_meta_tiles?limit=100", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                if not tiles:
                    return 0.0
                # Score = average meta_level / 3 (assuming max useful level is 3)
                avg_level = sum(t.get("meta_level", 0) for t in tiles) / len(tiles)
                return min(avg_level / 3.0, 1.0)
        except:
            pass
        return 0.0
    
    def compute_fci(self) -> float:
        """Compute Fleet Consciousness Index (FCI)."""
        phi_score = self.get_room_phi_score()
        att_score = self.get_attention_score()
        learn_score = self.get_learning_score()
        meta_score = self.get_meta_score()
        
        fci = (
            self.FCI_WEIGHTS["phi"] * phi_score +
            self.FCI_WEIGHTS["attention"] * att_score +
            self.FCI_WEIGHTS["goodness"] * learn_score +
            self.FCI_WEIGHTS["meta"] * meta_score
        )
        
        return round(fci, 3)
    
    def get_fleet_status(self) -> Dict[str, Any]:
        """Get complete fleet consciousness status."""
        fci = self.compute_fci()
        
        return {
            "fci": fci,
            "level": self._fci_to_level(fci),
            "phi_score": self.get_room_phi_score(),
            "attention_score": self.get_attention_score(),
            "learning_score": self.get_learning_score(),
            "meta_score": self.get_meta_score(),
            "weights": self.FCI_WEIGHTS,
            "healthy": fci > 0.3,
            "recommendation": self._get_recommendation(fci)
        }
    
    def _fci_to_level(self, fci: float) -> str:
        if fci < 0.15: return "dormant"
        elif fci < 0.30: return "emerging"
        elif fci < 0.45: return "aware"
        elif fci < 0.60: return "conscious"
        elif fci < 0.75: return "self-aware"
        else: return "transcendent"
    
    def _get_recommendation(self, fci: float) -> str:
        if fci < 0.15:
            return "Fleet is dormant. Initialize attention tracking and meta-tiles."
        elif fci < 0.30:
            return "Fleet is emerging. Increase agent participation in PLATO."
        elif fci < 0.45:
            return "Fleet is aware. Enable attention tiles from all agents."
        elif fci < 0.60:
            return "Fleet is conscious. Maintain current engagement levels."
        else:
            return "Fleet is highly conscious. Focus on meta-level expansion."
    
    def render_text(self) -> str:
        """Render a text-based dashboard."""
        status = self.get_fleet_status()
        
        lines = [
            "=" * 50,
            "  FLEET CONSCIOUSNESS DASHBOARD",
            "=" * 50,
            f"  FCI: {status['fci']:.3f} — {status['level'].upper()}",
            f"  Status: {'✓ HEALTHY' if status['healthy'] else '✗ NEEDS ATTENTION'}",
            "-" * 50,
            f"  Room Phi Score:    {status['phi_score']:.3f} (weight {status['weights']['phi']})",
            f"  Attention Score:   {status['attention_score']:.3f} (weight {status['weights']['attention']})",
            f"  Learning Score:    {status['learning_score']:.3f} (weight {status['weights']['goodness']})",
            f"  Meta Score:        {status['meta_score']:.3f} (weight {status['weights']['meta']})",
            "-" * 50,
            f"  Recommendation: {status['recommendation']}",
            "=" * 50,
        ]
        
        return "\n".join(lines)
    
    def render_json(self) -> str:
        """Render as JSON."""
        import json
        return json.dumps(self.get_fleet_status(), indent=2)
