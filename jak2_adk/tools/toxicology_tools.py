"""ADMET & Hepatotoxicity / DILI risk evaluation tools."""

from typing import List
from ..config import DEFAULT_TPP, TargetProductProfile
from ..models import ToxicologyEvaluation


def screen_toxicology_alerts(
    clogp: float,
    hlm_half_life_min: float,
    cyp3a4_ic50_um: float,
    cyp2d6_ic50_um: float,
    cyp2c9_ic50_um: float,
    herg_ic50_um: float,
    reactive_metabolite_risk: bool,
    hepatotoxicity_alert: bool,
    pains_alert: bool,
    tpp: TargetProductProfile = DEFAULT_TPP
) -> ToxicologyEvaluation:
    """Screen for in vitro ADMET liabilities, structural alerts, and DILI risk factors."""
    liabilities: List[str] = []

    # Rule of Two risk (cLogP > 3.0 is a known cofactor for dose-dependent DILI)
    rule_of_two = clogp > tpp.clogp_ideal_max
    if rule_of_two:
        liabilities.append(f"Rule-of-Two DILI Risk: cLogP {clogp:.2f} > {tpp.clogp_ideal_max}")

    if reactive_metabolite_risk:
        liabilities.append("Reactive Metabolite Alert: Glutathione (GSH) adduct risk detected")

    if hepatotoxicity_alert:
        liabilities.append("Structural DILI Alert: Core scaffold flags HepG2 cytotoxicity risk")

    if pains_alert:
        liabilities.append("PAINS Alert: Pan-Assay Interference motif detected")

    # CYP inhibition check
    cyp_clean = True
    for cyp_name, val in [("CYP3A4", cyp3a4_ic50_um), ("CYP2D6", cyp2d6_ic50_um), ("CYP2C9", cyp2c9_ic50_um)]:
        if val < tpp.cyp_inhibition_ic50_min_um:
            cyp_clean = False
            liabilities.append(f"{cyp_name} Liability: IC50 {val:.1f} µM < {tpp.cyp_inhibition_ic50_min_um} µM")

    # Metabolic stability check
    stability_ok = hlm_half_life_min >= tpp.hlm_half_life_acceptable_min_min
    if not stability_ok:
        liabilities.append(
            f"Metabolic Clearance Liability: HLM T1/2 {hlm_half_life_min:.1f} min < {tpp.hlm_half_life_acceptable_min_min} min"
        )

    # hERG liability check
    herg_clean = herg_ic50_um >= tpp.herg_ic50_min_um
    if not herg_clean:
        liabilities.append(f"hERG Cardiotoxicity Alert: IC50 {herg_ic50_um:.1f} µM < {tpp.herg_ic50_min_um} µM")

    # Overall DILI risk categorization
    if hepatotoxicity_alert or reactive_metabolite_risk or (rule_of_two and not cyp_clean):
        dili_level = "HIGH"
    elif rule_of_two or not cyp_clean or not stability_ok:
        dili_level = "MODERATE"
    else:
        dili_level = "LOW"

    return ToxicologyEvaluation(
        dili_risk_level=dili_level,
        rule_of_two_risk=rule_of_two,
        reactive_metabolites=reactive_metabolite_risk,
        cyp_inhibition_clean=cyp_clean,
        herg_clean=herg_clean,
        metabolic_stability_ok=stability_ok,
        identified_liabilities=liabilities
    )
