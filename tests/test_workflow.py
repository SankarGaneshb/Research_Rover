"""Integration tests for the JAK2 screening cascade orchestrator and Google ADK agent."""

import pytest
from jak2_adk.models import CandidateInput, DecisionVerdict
from jak2_adk.workflow import JAK2ScreeningOrchestrator


@pytest.fixture
def orchestrator():
    return JAK2ScreeningOrchestrator()


@pytest.fixture
def lead_candidate():
    return CandidateInput(
        candidate_id="LEAD-001",
        mw=410.0,
        clogp=2.2,
        tpsa=84.0,
        hbd=2,
        hba=5,
        rot_bonds=4,
        heavy_atom_count=30,
        jak2_ic50_nm=5.0,
        jak1_ic50_nm=300.0,
        jak3_ic50_nm=500.0,
        tyk2_ic50_nm=120.0,
        cellular_pstat5_ic50_nm=35.0,
        hlm_half_life_min=65.0,
        solubility_ug_ml=55.0,
        cyp3a4_ic50_um=25.0,
        cyp2d6_ic50_um=20.0,
        cyp2c9_ic50_um=18.0,
        herg_ic50_um=25.0,
        reactive_metabolite_risk=False,
        hepatotoxicity_alert=False,
        pains_alert=False
    )


@pytest.fixture
def greasy_candidate():
    return CandidateInput(
        candidate_id="GREASY-002",
        mw=510.0,
        clogp=4.8,
        tpsa=55.0,
        hbd=1,
        hba=4,
        rot_bonds=8,
        heavy_atom_count=38,
        jak2_ic50_nm=8.0,
        jak1_ic50_nm=40.0,
        jak3_ic50_nm=60.0,
        tyk2_ic50_nm=20.0,
        cellular_pstat5_ic50_nm=220.0,
        hlm_half_life_min=12.0,
        solubility_ug_ml=5.0,
        cyp3a4_ic50_um=2.5,
        cyp2d6_ic50_um=4.0,
        cyp2c9_ic50_um=3.0,
        herg_ic50_um=4.0,
        reactive_metabolite_risk=False,
        hepatotoxicity_alert=False,
        pains_alert=False
    )


@pytest.fixture
def tox_alert_candidate():
    return CandidateInput(
        candidate_id="TOX-003",
        mw=390.0,
        clogp=2.6,
        tpsa=80.0,
        hbd=2,
        hba=5,
        rot_bonds=4,
        heavy_atom_count=28,
        jak2_ic50_nm=8.0,
        jak1_ic50_nm=400.0,
        jak3_ic50_nm=600.0,
        tyk2_ic50_nm=150.0,
        cellular_pstat5_ic50_nm=50.0,
        hlm_half_life_min=45.0,
        solubility_ug_ml=40.0,
        cyp3a4_ic50_um=18.0,
        cyp2d6_ic50_um=15.0,
        cyp2c9_ic50_um=14.0,
        herg_ic50_um=20.0,
        reactive_metabolite_risk=True,
        hepatotoxicity_alert=True,
        pains_alert=False
    )


def test_evaluate_lead_candidate(orchestrator, lead_candidate):
    report = orchestrator.evaluate_candidate(lead_candidate)
    assert report.verdict == DecisionVerdict.ADVANCE
    assert report.composite_mpo >= 0.75
    assert report.efficiency.lipe >= 5.5
    assert report.efficiency.le >= 0.35
    assert report.toxicology.dili_risk_level == "LOW"
    assert len(report.gate_failures) == 0


def test_evaluate_greasy_candidate(orchestrator, greasy_candidate):
    report = orchestrator.evaluate_candidate(greasy_candidate)
    assert report.verdict in (DecisionVerdict.HOLD, DecisionVerdict.REJECT)
    assert report.composite_mpo < 0.60
    assert any("Lipophilicity trap" in f for f in report.gate_failures)


def test_evaluate_tox_alert_candidate(orchestrator, tox_alert_candidate):
    report = orchestrator.evaluate_candidate(tox_alert_candidate)
    assert report.verdict == DecisionVerdict.REJECT
    assert report.toxicology.dili_risk_level == "HIGH"
    assert any("Safety Gate" in f for f in report.gate_failures)


def test_build_adk_sequential_agent(orchestrator):
    adk_agent = orchestrator.build_adk_sequential_agent()
    assert adk_agent is not None
    assert adk_agent.name == "JAK2_Optimization_Cascade_Orchestrator"
    assert len(adk_agent.sub_agents) == 4
    sub_names = [sub.name for sub in adk_agent.sub_agents]
    assert "PhysChem_Efficiency_Specialist" in sub_names
    assert "Kinase_Potency_Selectivity_Specialist" in sub_names
    assert "ADMET_DILI_Safety_Specialist" in sub_names
    assert "MPO_Governance_Decision_Specialist" in sub_names
