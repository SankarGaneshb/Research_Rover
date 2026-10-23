"""Multi-Parameter Optimization (MPO) scoring engine using continuous desirability functions."""

from typing import Dict, Any, Tuple
from ..config import DEFAULT_TPP, TargetProductProfile
from ..models import CandidateInput, EfficiencyMetrics, SelectivityMetrics, ToxicologyEvaluation, MPOScores, DecisionVerdict


def _ramp(val: float, low: float, high: float, reverse: bool = False) -> float:
    """Linear desirability ramp between 0.0 and 1.0."""
    if low == high:
        return 1.0 if val >= high else 0.0
    if not reverse:
        if val <= low:
            return 0.0
        if val >= high:
            return 1.0
        return (val - low) / (high - low)
    else:
        # reverse: lower is better (e.g. IC50, cLogP)
        if val >= high:
            return 0.0
        if val <= low:
            return 1.0
        return (high - val) / (high - low)


def compute_mpo_score(
    candidate: CandidateInput,
    efficiency: EfficiencyMetrics,
    selectivity: SelectivityMetrics,
    toxicology: ToxicologyEvaluation,
    tpp: TargetProductProfile = DEFAULT_TPP
) -> Tuple[MPOScores, DecisionVerdict, list[str]]:
    """Compute individual pillar scores, composite MPO score, and gate verdict."""
    gate_failures = []

    # 1. Potency Score (JAK2 biochemical + pSTAT5 cellular)
    s_jak2 = _ramp(candidate.jak2_ic50_nm, tpp.jak2_enzymatic_ideal_max_nm, tpp.jak2_enzymatic_acceptable_max_nm, reverse=True)
    s_pstat5 = _ramp(candidate.cellular_pstat5_ic50_nm, tpp.jak2_cellular_pstat5_ideal_max_nm, tpp.jak2_cellular_pstat5_acceptable_max_nm, reverse=True)
    potency_score = round(0.5 * s_jak2 + 0.5 * s_pstat5, 3)

    if candidate.jak2_ic50_nm > tpp.jak2_enzymatic_acceptable_max_nm:
        gate_failures.append(f"JAK2 Potency Gate: {candidate.jak2_ic50_nm} nM > {tpp.jak2_enzymatic_acceptable_max_nm} nM limit")

    # 2. Selectivity Score
    s_jak1 = _ramp(selectivity.jak1_fold, 1.0, tpp.selectivity_jak1_fold_min, reverse=False)
    s_jak3 = _ramp(selectivity.jak3_fold, 1.0, tpp.selectivity_jak3_fold_min, reverse=False)
    s_tyk2 = _ramp(selectivity.tyk2_fold, 1.0, tpp.selectivity_tyk2_fold_min, reverse=False)
    selectivity_score = round(0.4 * s_jak1 + 0.4 * s_jak3 + 0.2 * s_tyk2, 3)

    if not selectivity.passes_selectivity_gate:
        gate_failures.append(f"Selectivity Gate: Insufficient window ({selectivity.selectivity_summary})")

    # 3. Safety & DILI Score
    s_dili = 1.0 if toxicology.dili_risk_level == "LOW" else (0.5 if toxicology.dili_risk_level == "MODERATE" else 0.0)
    s_reactive = 0.0 if candidate.reactive_metabolite_risk else 1.0
    s_cyp = 1.0 if toxicology.cyp_inhibition_clean else 0.4
    s_herg = 1.0 if toxicology.herg_clean else 0.2
    safety_dili_score = round(0.35 * s_dili + 0.25 * s_reactive + 0.25 * s_cyp + 0.15 * s_herg, 3)

    if candidate.reactive_metabolite_risk or candidate.hepatotoxicity_alert:
        gate_failures.append("Safety Gate: Severe structural hepatotoxicity or reactive metabolite flag")

    # 4. PhysChem & Efficiency Score
    s_clogp = _ramp(candidate.clogp, tpp.clogp_ideal_max, tpp.clogp_acceptable_max, reverse=True)
    s_mw = _ramp(candidate.mw, tpp.mw_ideal_max, tpp.mw_acceptable_max, reverse=True)
    s_lipe = _ramp(efficiency.lipe, tpp.lipe_acceptable_min, tpp.lipe_ideal_min, reverse=False)
    s_le = _ramp(efficiency.le, tpp.le_acceptable_min, tpp.le_ideal_min, reverse=False)
    physchem_score = round(0.3 * s_clogp + 0.2 * s_mw + 0.3 * s_lipe + 0.2 * s_le, 3)

    if candidate.clogp > tpp.clogp_acceptable_max:
        gate_failures.append(f"PhysChem Gate: Lipophilicity trap cLogP {candidate.clogp} > {tpp.clogp_acceptable_max}")

    # 5. Developability Score (Solubility + HLM stability)
    s_sol = _ramp(candidate.solubility_ug_ml, tpp.solubility_acceptable_min_ug_ml, tpp.solubility_ideal_min_ug_ml, reverse=False)
    s_hlm = _ramp(candidate.hlm_half_life_min, tpp.hlm_half_life_acceptable_min_min, tpp.hlm_half_life_ideal_min_min, reverse=False)
    developability_score = round(0.5 * s_sol + 0.5 * s_hlm, 3)

    # Composite MPO
    w = tpp.weights
    composite_mpo = round(
        w["potency"] * potency_score +
        w["selectivity"] * selectivity_score +
        w["safety_dili"] * safety_dili_score +
        w["physchem"] * physchem_score +
        w["developability"] * developability_score,
        3
    )

    # Decision verdict
    if len(gate_failures) == 0 and composite_mpo >= tpp.mpo_advance_threshold:
        verdict = DecisionVerdict.ADVANCE
    elif any("Severe structural" in f or "Lipophilicity trap" in f for f in gate_failures) or composite_mpo < tpp.mpo_hold_threshold:
        verdict = DecisionVerdict.REJECT
    else:
        verdict = DecisionVerdict.HOLD

    scores = MPOScores(
        potency_score=potency_score,
        selectivity_score=selectivity_score,
        safety_dili_score=safety_dili_score,
        physchem_score=physchem_score,
        developability_score=developability_score,
        composite_mpo=composite_mpo
    )

    return scores, verdict, gate_failures
