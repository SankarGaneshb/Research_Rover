"""Validation tests for Pydantic data schemas."""

import pytest
from pydantic import ValidationError
from jak2_adk.models import CandidateInput, DecisionVerdict


def test_candidate_input_valid():
    candidate = CandidateInput(
        candidate_id="TEST-001",
        mw=400.0,
        clogp=2.5,
        tpsa=80.0,
        hbd=2,
        hba=5,
        rot_bonds=4,
        heavy_atom_count=29,
        jak2_ic50_nm=10.0,
        jak1_ic50_nm=300.0,
        jak3_ic50_nm=500.0,
        tyk2_ic50_nm=100.0,
        cellular_pstat5_ic50_nm=60.0,
        hlm_half_life_min=45.0,
        solubility_ug_ml=40.0,
        cyp3a4_ic50_um=20.0,
        cyp2d6_ic50_um=15.0,
        cyp2c9_ic50_um=12.0,
        herg_ic50_um=25.0
    )
    assert candidate.candidate_id == "TEST-001"
    assert candidate.reactive_metabolite_risk is False


def test_candidate_input_missing_required():
    with pytest.raises(ValidationError):
        CandidateInput(
            candidate_id="INVALID-001",
            mw=400.0
            # missing required fields
        )
