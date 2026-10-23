"""Pydantic data models for candidate input and multi-agent evaluation output."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DecisionVerdict(str, Enum):
    ADVANCE = "ADVANCE_TO_IN_VIVO"
    HOLD = "HOLD_FOR_OPTIMIZATION"
    REJECT = "REJECT_CRITICAL_LIABILITY"


class CandidateInput(BaseModel):
    """Input representation of a kinase inhibitor candidate."""
    candidate_id: str = Field(..., description="Unique candidate identifier")
    smiles: Optional[str] = Field(None, description="Simplified molecular representation or scaffold identifier")
    
    # Physicochemical properties
    mw: float = Field(..., description="Molecular weight (g/mol)")
    clogp: float = Field(..., description="Calculated logP / lipophilicity")
    tpsa: float = Field(..., description="Topological polar surface area (Å²)")
    hbd: int = Field(..., description="Hydrogen bond donors count")
    hba: int = Field(..., description="Hydrogen bond acceptors count")
    rot_bonds: int = Field(..., description="Number of rotatable bonds")
    heavy_atom_count: int = Field(..., description="Number of non-hydrogen atoms")

    # Biochemical Potency (nM)
    jak2_ic50_nm: float = Field(..., description="Biochemical JAK2 enzymatic IC50 (nM)")
    jak1_ic50_nm: float = Field(..., description="Biochemical JAK1 enzymatic IC50 (nM)")
    jak3_ic50_nm: float = Field(..., description="Biochemical JAK3 enzymatic IC50 (nM)")
    tyk2_ic50_nm: float = Field(..., description="Biochemical TYK2 enzymatic IC50 (nM)")
    cellular_pstat5_ic50_nm: float = Field(..., description="Cellular target engagement pSTAT5 IC50 (nM)")

    # In Vitro ADMET & Safety Readouts
    hlm_half_life_min: float = Field(..., description="Human Liver Microsomal half-life (min)")
    solubility_ug_ml: float = Field(..., description="Thermodynamic aqueous solubility at pH 6.5 (µg/mL)")
    cyp3a4_ic50_um: float = Field(..., description="CYP3A4 inhibition IC50 (µM)")
    cyp2d6_ic50_um: float = Field(..., description="CYP2D6 inhibition IC50 (µM)")
    cyp2c9_ic50_um: float = Field(..., description="CYP2C9 inhibition IC50 (µM)")
    herg_ic50_um: float = Field(..., description="hERG patch clamp IC50 (µM)")
    
    # Alerts / flags
    reactive_metabolite_risk: bool = Field(False, description="Flag for reactive metabolite formation (e.g. GSH trapping alert)")
    hepatotoxicity_alert: bool = Field(False, description="Flag for structural DILI liability or HepG2 cytotoxicity alert")
    pains_alert: bool = Field(False, description="Flag for Pan-Assay Interference (PAINS) motif")


class EfficiencyMetrics(BaseModel):
    pic50_jak2: float
    lipe: float
    le: float
    bei: float
    passes_efficiency_gate: bool


class SelectivityMetrics(BaseModel):
    jak1_fold: float
    jak3_fold: float
    tyk2_fold: float
    passes_selectivity_gate: bool
    selectivity_summary: str


class ToxicologyEvaluation(BaseModel):
    dili_risk_level: str  # "LOW", "MODERATE", "HIGH"
    rule_of_two_risk: bool
    reactive_metabolites: bool
    cyp_inhibition_clean: bool
    herg_clean: bool
    metabolic_stability_ok: bool
    identified_liabilities: List[str] = []


class MPOScores(BaseModel):
    potency_score: float = Field(..., ge=0.0, le=1.0)
    selectivity_score: float = Field(..., ge=0.0, le=1.0)
    safety_dili_score: float = Field(..., ge=0.0, le=1.0)
    physchem_score: float = Field(..., ge=0.0, le=1.0)
    developability_score: float = Field(..., ge=0.0, le=1.0)
    composite_mpo: float = Field(..., ge=0.0, le=1.0)


class CandidateEvaluationReport(BaseModel):
    candidate_id: str
    verdict: DecisionVerdict
    composite_mpo: float
    efficiency: EfficiencyMetrics
    selectivity: SelectivityMetrics
    toxicology: ToxicologyEvaluation
    mpo_scores: MPOScores
    gate_failures: List[str] = []
    agent_reasoning: Dict[str, str] = {}
