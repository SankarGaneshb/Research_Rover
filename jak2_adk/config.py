"""Target Product Profile (TPP) configuration and screening cascade thresholds for JAK2."""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class TargetProductProfile:
    """Target Product Profile (TPP) criteria and threshold limits."""

    # Physicochemical Boundaries
    clogp_ideal_max: float = 3.0
    clogp_acceptable_max: float = 3.5
    mw_ideal_max: float = 450.0
    mw_acceptable_max: float = 500.0
    tpsa_min: float = 60.0
    tpsa_max: float = 120.0
    hbd_max: int = 3
    hba_max: int = 7
    rot_bonds_max: int = 7

    # Efficiency Targets
    lipe_ideal_min: float = 5.5
    lipe_acceptable_min: float = 4.5
    le_ideal_min: float = 0.38
    le_acceptable_min: float = 0.32

    # Potency Targets (nM)
    jak2_enzymatic_ideal_max_nm: float = 10.0
    jak2_enzymatic_acceptable_max_nm: float = 50.0
    jak2_cellular_pstat5_ideal_max_nm: float = 100.0
    jak2_cellular_pstat5_acceptable_max_nm: float = 250.0

    # Isoform Selectivity (fold-window over JAK2)
    selectivity_jak1_fold_min: float = 30.0
    selectivity_jak3_fold_min: float = 50.0
    selectivity_tyk2_fold_min: float = 10.0

    # In Vitro ADMET & Safety
    hlm_half_life_ideal_min_min: float = 60.0
    hlm_half_life_acceptable_min_min: float = 30.0
    cyp_inhibition_ic50_min_um: float = 10.0
    herg_ic50_min_um: float = 10.0
    solubility_ideal_min_ug_ml: float = 50.0
    solubility_acceptable_min_ug_ml: float = 20.0

    # MPO Weightings across 5 pillars
    weights: Dict[str, float] = field(default_factory=lambda: {
        "potency": 0.35,
        "selectivity": 0.20,
        "safety_dili": 0.25,
        "physchem": 0.10,
        "developability": 0.10
    })

    # Decision Gate Thresholds
    mpo_advance_threshold: float = 0.75
    mpo_hold_threshold: float = 0.50


# Global default instance
DEFAULT_TPP = TargetProductProfile()
