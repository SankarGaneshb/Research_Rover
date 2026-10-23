"""ADMET & Hepatotoxicity / DILI Safety Agent."""

from typing import Tuple, Optional, Any
from ..models import CandidateInput, ToxicologyEvaluation
from ..config import DEFAULT_TPP, TargetProductProfile
from ..tools.toxicology_tools import screen_toxicology_alerts


class ToxAgent:
    """Agent responsible for Tier 3: In vitro ADMET, hepatotoxicity (DILI), reactive metabolites, and safety alerts."""

    NAME = "ADMET_DILI_Safety_Specialist"
    ROLE = "Toxicology, Metabolic Stability, and Hepatotoxicity Specialist"

    INSTRUCTIONS = (
        "You are an expert drug safety and ADMET toxicologist. "
        "Your mission is to rigorously de-risk kinase inhibitors against drug-induced liver injury (DILI) "
        "and metabolic liabilities. Evaluate against: Rule-of-Two (cLogP > 3.0), reactive metabolites (GSH adducts), "
        "CYP inhibition (3A4, 2D6, 2C9 IC50 >= 10 µM), microsomal stability (HLM T1/2 >= 30 min), "
        "and hERG cardiotoxicity (IC50 >= 10 µM). Enforce strict zero-tolerance for reactive toxicophores."
    )

    def __init__(self, tpp: TargetProductProfile = DEFAULT_TPP):
        self.tpp = tpp

    def analyze(self, candidate: CandidateInput) -> Tuple[ToxicologyEvaluation, str]:
        """Perform deterministic toxicology screening and safety reasoning."""
        evaluation = screen_toxicology_alerts(
            clogp=candidate.clogp,
            hlm_half_life_min=candidate.hlm_half_life_min,
            cyp3a4_ic50_um=candidate.cyp3a4_ic50_um,
            cyp2d6_ic50_um=candidate.cyp2d6_ic50_um,
            cyp2c9_ic50_um=candidate.cyp2c9_ic50_um,
            herg_ic50_um=candidate.herg_ic50_um,
            reactive_metabolite_risk=candidate.reactive_metabolite_risk,
            hepatotoxicity_alert=candidate.hepatotoxicity_alert,
            pains_alert=candidate.pains_alert,
            tpp=self.tpp
        )

        reasoning_lines = [
            f"[{self.NAME}] Safety evaluation for candidate {candidate.candidate_id}:",
            f"- DILI Risk Tier: {evaluation.dili_risk_level}",
            f"- Metabolic Stability: HLM T1/2 {candidate.hlm_half_life_min:.1f} min (Target >= {self.tpp.hlm_half_life_acceptable_min_min} min)",
            f"- CYP Inhibition Status: {'Clean' if evaluation.cyp_inhibition_clean else 'FLAGGED'}",
            f"- hERG Status: {'Clean' if evaluation.herg_clean else 'FLAGGED'} (IC50 {candidate.herg_ic50_um:.1f} µM)",
        ]

        if evaluation.identified_liabilities:
            reasoning_lines.append("  ⚠️ IDENTIFIED SAFETY LIABILITIES:")
            for liability in evaluation.identified_liabilities:
                reasoning_lines.append(f"    * {liability}")
        else:
            reasoning_lines.append("  ✅ SAFETY PROFILE CLEAN: No critical structural or metabolic flags.")

        return evaluation, "\n".join(reasoning_lines)

    def create_adk_agent(self, model: str = "gemini-2.5-flash") -> Optional[Any]:
        """Instantiate a Google ADK Agent object."""
        try:
            from google.adk.agents import Agent
            return Agent(
                name=self.NAME,
                model=model,
                instruction=self.INSTRUCTIONS,
                tools=[screen_toxicology_alerts]
            )
        except (ImportError, Exception):
            return None
