"""Tests for FleetDashboard FCI computation."""

import pytest
from unittest.mock import patch, MagicMock
from fleet_dashboard import FleetDashboard


class TestFCIComputation:
    """Test FCI calculation with mock scores."""

    @patch.object(FleetDashboard, 'get_room_phi_score')
    @patch.object(FleetDashboard, 'get_attention_score')
    @patch.object(FleetDashboard, 'get_learning_score')
    @patch.object(FleetDashboard, 'get_meta_score')
    def test_fci_full_scores(self, mock_meta, mock_learn, mock_att, mock_phi):
        """FCI = 0.4*1.0 + 0.2*1.0 + 0.25*1.0 + 0.15*1.0 = 1.0"""
        mock_phi.return_value = 1.0
        mock_att.return_value = 1.0
        mock_learn.return_value = 1.0
        mock_meta.return_value = 1.0

        dashboard = FleetDashboard()
        fci = dashboard.compute_fci()
        assert fci == 1.0

    @patch.object(FleetDashboard, 'get_room_phi_score')
    @patch.object(FleetDashboard, 'get_attention_score')
    @patch.object(FleetDashboard, 'get_learning_score')
    @patch.object(FleetDashboard, 'get_meta_score')
    def test_fci_zero_scores(self, mock_meta, mock_learn, mock_att, mock_phi):
        """FCI = 0.4*0 + 0.2*0 + 0.25*0 + 0.15*0 = 0.0"""
        mock_phi.return_value = 0.0
        mock_att.return_value = 0.0
        mock_learn.return_value = 0.0
        mock_meta.return_value = 0.0

        dashboard = FleetDashboard()
        fci = dashboard.compute_fci()
        assert fci == 0.0

    @patch.object(FleetDashboard, 'get_room_phi_score')
    @patch.object(FleetDashboard, 'get_attention_score')
    @patch.object(FleetDashboard, 'get_learning_score')
    @patch.object(FleetDashboard, 'get_meta_score')
    def test_fci_mixed_scores(self, mock_meta, mock_learn, mock_att, mock_phi):
        """FCI = 0.4*0.5 + 0.2*0.5 + 0.25*0.5 + 0.15*0.5 = 0.5"""
        mock_phi.return_value = 0.5
        mock_att.return_value = 0.5
        mock_learn.return_value = 0.5
        mock_meta.return_value = 0.5

        dashboard = FleetDashboard()
        fci = dashboard.compute_fci()
        assert fci == 0.5

    @patch.object(FleetDashboard, 'get_room_phi_score')
    @patch.object(FleetDashboard, 'get_attention_score')
    @patch.object(FleetDashboard, 'get_learning_score')
    @patch.object(FleetDashboard, 'get_meta_score')
    def test_fci_default_baseline(self, mock_meta, mock_learn, mock_att, mock_phi):
        """Defaults: phi=0.3, att=0.2, learn=0.5, meta=0.0
        FCI = 0.4*0.3 + 0.2*0.2 + 0.25*0.5 + 0.15*0.0 = 0.12+0.04+0.125+0 = 0.31"""
        mock_phi.return_value = 0.3
        mock_att.return_value = 0.2
        mock_learn.return_value = 0.5
        mock_meta.return_value = 0.0

        dashboard = FleetDashboard()
        fci = dashboard.compute_fci()
        assert abs(fci - 0.310) < 0.01


class TestConsciousnessLevels:
    """Test FCI level classification."""

    def test_level_dormant(self):
        dashboard = FleetDashboard()
        assert dashboard._fci_to_level(0.10) == "dormant"

    def test_level_emerging(self):
        dashboard = FleetDashboard()
        assert dashboard._fci_to_level(0.20) == "emerging"

    def test_level_aware(self):
        dashboard = FleetDashboard()
        assert dashboard._fci_to_level(0.35) == "aware"

    def test_level_conscious(self):
        dashboard = FleetDashboard()
        assert dashboard._fci_to_level(0.50) == "conscious"

    def test_level_self_aware(self):
        dashboard = FleetDashboard()
        assert dashboard._fci_to_level(0.65) == "self-aware"

    def test_level_transcendent(self):
        dashboard = FleetDashboard()
        assert dashboard._fci_to_level(0.85) == "transcendent"


class TestHealthStatus:
    """Test health flag logic."""

    @patch.object(FleetDashboard, 'get_room_phi_score')
    @patch.object(FleetDashboard, 'get_attention_score')
    @patch.object(FleetDashboard, 'get_learning_score')
    @patch.object(FleetDashboard, 'get_meta_score')
    def test_healthy_when_fci_above_threshold(self, mock_meta, mock_learn, mock_att, mock_phi):
        mock_phi.return_value = 0.5
        mock_att.return_value = 0.5
        mock_learn.return_value = 0.5
        mock_meta.return_value = 0.5

        dashboard = FleetDashboard()
        status = dashboard.get_fleet_status()
        assert status["healthy"] is True

    @patch.object(FleetDashboard, 'get_room_phi_score')
    @patch.object(FleetDashboard, 'get_attention_score')
    @patch.object(FleetDashboard, 'get_learning_score')
    @patch.object(FleetDashboard, 'get_meta_score')
    def test_unhealthy_when_fci_below_threshold(self, mock_meta, mock_learn, mock_att, mock_phi):
        mock_phi.return_value = 0.1
        mock_att.return_value = 0.1
        mock_learn.return_value = 0.1
        mock_meta.return_value = 0.0

        dashboard = FleetDashboard()
        status = dashboard.get_fleet_status()
        assert status["healthy"] is False
