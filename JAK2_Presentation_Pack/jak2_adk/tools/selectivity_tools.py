"""Isoform selectivity evaluators across the JAK family (JAK1, JAK2, JAK3, TYK2)."""

from typing import Dict, Any
from ..config import DEFAULT_TPP, TargetProductProfile
from ..models import SelectivityMetrics


def evaluate_selectivity_ratios(
    jak2_ic50_nm: float,
    jak1_ic50_nm: float,
    jak3_ic50_nm: float,
    tyk2_ic50_nm: float,
    tpp: TargetProductProfile = DEFAULT_TPP
) -> SelectivityMetrics:
    """Calculate fold selectivity over JAK2 for JAK1, JAK3, and TYK2.
    
    Fold selectivity is defined as IC50(off-target) / IC50(JAK2).
    A fold > 1 indicates selectivity toward JAK2.
    """
    if jak2_ic50_nm <= 0:
        raise ValueError("jak2_ic50_nm must be positive")

    jak1_fold = jak1_ic50_nm / jak2_ic50_nm
    jak3_fold = jak3_ic50_nm / jak2_ic50_nm
    tyk2_fold = tyk2_ic50_nm / jak2_ic50_nm

    passes_jak1 = jak1_fold >= tpp.selectivity_jak1_fold_min
    passes_jak3 = jak3_fold >= tpp.selectivity_jak3_fold_min
    passes_tyk2 = tyk2_fold >= tpp.selectivity_tyk2_fold_min

    passes_gate = passes_jak1 and passes_jak3 and passes_tyk2

    summary_parts = []
    if passes_jak1:
        summary_parts.append(f"JAK1: {jak1_fold:.1f}x (>= {tpp.selectivity_jak1_fold_min}x)")
    else:
        summary_parts.append(f"JAK1 FAIL: {jak1_fold:.1f}x (< {tpp.selectivity_jak1_fold_min}x)")

    if passes_jak3:
        summary_parts.append(f"JAK3: {jak3_fold:.1f}x (>= {tpp.selectivity_jak3_fold_min}x)")
    else:
        summary_parts.append(f"JAK3 FAIL: {jak3_fold:.1f}x (< {tpp.selectivity_jak3_fold_min}x)")

    if passes_tyk2:
        summary_parts.append(f"TYK2: {tyk2_fold:.1f}x (>= {tpp.selectivity_tyk2_fold_min}x)")
    else:
        summary_parts.append(f"TYK2 FAIL: {tyk2_fold:.1f}x (< {tpp.selectivity_tyk2_fold_min}x)")

    return SelectivityMetrics(
        jak1_fold=round(jak1_fold, 1),
        jak3_fold=round(jak3_fold, 1),
        tyk2_fold=round(tyk2_fold, 1),
        passes_selectivity_gate=passes_gate,
        selectivity_summary=" | ".join(summary_parts)
    )
