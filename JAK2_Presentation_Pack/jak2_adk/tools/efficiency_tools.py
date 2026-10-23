"""Binding efficiency calculators: LipE, LE, and BEI."""

import math
from typing import Dict, Any
from ..config import DEFAULT_TPP, TargetProductProfile
from ..models import EfficiencyMetrics


def calculate_efficiency_metrics(
    jak2_ic50_nm: float,
    clogp: float,
    heavy_atom_count: int,
    mw: float,
    tpp: TargetProductProfile = DEFAULT_TPP
) -> EfficiencyMetrics:
    """Calculate pIC50, LipE, LE, and BEI for a kinase inhibitor candidate.
    
    Formulae:
    - pIC50 = 9 - log10(IC50 in nM)
    - LipE = pIC50 - clogP
    - LE = 1.37 * pIC50 / HAC (kcal/mol/heavy atom)
    - BEI = pIC50 / (MW in kDa)
    """
    if jak2_ic50_nm <= 0:
        raise ValueError("jak2_ic50_nm must be positive")
    if heavy_atom_count <= 0:
        raise ValueError("heavy_atom_count must be positive")
    if mw <= 0:
        raise ValueError("mw must be positive")

    pic50 = 9.0 - math.log10(jak2_ic50_nm)
    lipe = pic50 - clogp
    le = (1.37 * pic50) / heavy_atom_count
    bei = pic50 / (mw / 1000.0)

    # Gate check against acceptable limits
    passes = (lipe >= tpp.lipe_acceptable_min) and (le >= tpp.le_acceptable_min)

    return EfficiencyMetrics(
        pic50_jak2=round(pic50, 2),
        lipe=round(lipe, 2),
        le=round(le, 3),
        bei=round(bei, 2),
        passes_efficiency_gate=passes
    )
