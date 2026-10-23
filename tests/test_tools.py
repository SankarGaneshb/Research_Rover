"""Unit tests for deterministic screening tools (LipE, Selectivity, Tox, MPO)."""

import pytest
from jak2_adk.tools.efficiency_tools import calculate_efficiency_metrics
from jak2_adk.tools.selectivity_tools import evaluate_selectivity_ratios
from jak2_adk.tools.toxicology_tools import screen_toxicology_alerts
from jak2_adk.tools.mpo_tools import compute_mpo_score
from jak2_adk.models import CandidateInput, DecisionVerdict


def test_calculate_efficiency_metrics():
    # 10 nM IC50 -> pIC50 = 8.0. clogP = 2.5 -> LipE = 5.5. HAC = 28 -> LE = (1.37 * 8) / 28 = 0.391
    metrics = calculate_efficiency_metrics(
        jak2_ic50_nm=10.0,
        clogp=2.5,
        heavy_atom_count=28,
        mw=380.0
    )
    assert metrics.pic50_jak2 == 8.0
    assert metrics.lipe == 5.5
    assert metrics.le == pytest.approx(0.391, abs=0.01)
    assert metrics.passes_efficiency_gate is True


def test_calculate_efficiency_gate_failure():
    # Greasy molecule: 100 nM IC50 -> pIC50 = 7.0. clogP = 4.5 -> LipE = 2.5 (< 4.5 limit)
    metrics = calculate_efficiency_metrics(
        jak2_ic50_nm=100.0,
        clogp=4.5,
        heavy_atom_count=35,
        mw=480.0
    )
    assert metrics.pic50_jak2 == 7.0
    assert metrics.lipe == 2.5
    assert metrics.passes_efficiency_gate is False


def test_evaluate_selectivity_ratios():
    metrics = evaluate_selectivity_ratios(
        jak2_ic50_nm=5.0,
        jak1_ic50_nm=250.0,   # 50x (>= 30x)
        jak3_ic50_nm=400.0,   # 80x (>= 50x)
        tyk2_ic50_nm=100.0    # 20x (>= 10x)
    )
    assert metrics.jak1_fold == 50.0
    assert metrics.jak3_fold == 80.0
    assert metrics.tyk2_fold == 20.0
    assert metrics.passes_selectivity_gate is True


def test_evaluate_selectivity_failure():
    metrics = evaluate_selectivity_ratios(
        jak2_ic50_nm=5.0,
        jak1_ic50_nm=20.0,    # 4x (< 30x)
        jak3_ic50_nm=50.0,    # 10x (< 50x)
        tyk2_ic50_nm=10.0     # 2x (< 10x)
    )
    assert metrics.passes_selectivity_gate is False
    assert "JAK1 FAIL" in metrics.selectivity_summary


def test_screen_toxicology_alerts_clean():
    tox = screen_toxicology_alerts(
        clogp=2.4,
        hlm_half_life_min=65.0,
        cyp3a4_ic50_um=25.0,
        cyp2d6_ic50_um=20.0,
        cyp2c9_ic50_um=15.0,
        herg_ic50_um=30.0,
        reactive_metabolite_risk=False,
        hepatotoxicity_alert=False,
        pains_alert=False
    )
    assert tox.dili_risk_level == "LOW"
    assert tox.cyp_inhibition_clean is True
    assert tox.rule_of_two_risk is False
    assert len(tox.identified_liabilities) == 0


def test_screen_toxicology_alerts_high_risk():
    tox = screen_toxicology_alerts(
        clogp=4.2,
        hlm_half_life_min=10.0,
        cyp3a4_ic50_um=2.0,
        cyp2d6_ic50_um=1.5,
        cyp2c9_ic50_um=3.0,
        herg_ic50_um=2.5,
        reactive_metabolite_risk=True,
        hepatotoxicity_alert=True,
        pains_alert=False
    )
    assert tox.dili_risk_level == "HIGH"
    assert tox.cyp_inhibition_clean is False
    assert tox.rule_of_two_risk is True
    assert len(tox.identified_liabilities) >= 4
