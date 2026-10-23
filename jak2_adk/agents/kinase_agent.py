"""Target Potency & Selectivity Agent for the JAK family."""

from typing import Tuple, Optional, Any
from ..models import CandidateInput, SelectivityMetrics
from ..config import DEFAULT_TPP, TargetProductProfile
from ..tools.selectivity_tools import evaluate_selectivity_ratios


class KinaseAgent:
    """Agent responsible for Tier 2: JAK2 enzymatic/cellular potency and isoform selectivity."""

    NAME = "Kinase_Potency_Selectivity_Specialist"
    ROLE = "JAK Kinome Potency and Isoform Selectivity Specialist"

    INSTRUCTIONS = (
        "You are an expert kinase medicinal chemist and structural biologist specializing in Janus kinases (JAK1, JAK2, JAK3, TYK2). "
        "Your mission is to evaluate target engagement for JAK2 (IC50 < 10 nM ideal, < 50 nM acceptable; cellular pSTAT5 < 100 nM) "
        "and enforce isoform selectivity windows (>= 30x over JAK1, >= 50x over JAK3, >= 10x over TYK2). "
        "Identify risks of immunosuppression caused by poor selectivity against JAK1/JAK3."
    )

    def __init__(self, tpp: TargetProductProfile = DEFAULT_TPP):
        self.tpp = tpp

    def analyze(self, candidate: CandidateInput) -> Tuple[SelectivityMetrics, str]:
        """Perform deterministic selectivity calculation and scientific reasoning."""
        metrics = evaluate_selectivity_ratios(
            jak2_ic50_nm=candidate.jak2_ic50_nm,
            jak1_ic50_nm=candidate.jak1_ic50_nm,
            jak3_ic50_nm=candidate.jak3_ic50_nm,
            tyk2_ic50_nm=candidate.tyk2_ic50_nm,
            tpp=self.tpp
        )

        reasoning_lines = [
            f"[{self.NAME}] Evaluation for candidate {candidate.candidate_id}:",
            f"- JAK2 Enzymatic IC50: {candidate.jak2_ic50_nm:.1f} nM (Target <= {self.tpp.jak2_enzymatic_acceptable_max_nm} nM)",
            f"- Cellular pSTAT5 IC50: {candidate.cellular_pstat5_ic50_nm:.1f} nM (Target <= {self.tpp.jak2_cellular_pstat5_acceptable_max_nm} nM)",
            f"- Isoform Selectivity Folds: {metrics.selectivity_summary}"
        ]

        if candidate.jak2_ic50_nm > self.tpp.jak2_enzymatic_acceptable_max_nm:
            reasoning_lines.append(
                f"  ❌ POTENCY FAILURE: Biochemical potency of {candidate.jak2_ic50_nm:.1f} nM fails target threshold."
            )
        elif candidate.cellular_pstat5_ic50_nm > self.tpp.jak2_cellular_pstat5_acceptable_max_nm:
            reasoning_lines.append(
                f"  ⚠️ CELLULAR ENGAGEMENT WARNING: Weak translation to cellular pSTAT5 inhibition ({candidate.cellular_pstat5_ic50_nm:.1f} nM)."
            )

        if not metrics.passes_selectivity_gate:
            reasoning_lines.append(
                "  ❌ SELECTIVITY GATE FAILED: Inadequate margin against off-target JAK isoforms; risk of pan-JAK immunosuppression."
            )
        else:
            reasoning_lines.append(
                "  ✅ SELECTIVITY GATE PASSED: Clean selectivity window sparing JAK1, JAK3, and TYK2."
            )

        return metrics, "\n".join(reasoning_lines)

    def create_adk_agent(self, model: str = "gemini-2.5-flash") -> Optional[Any]:
        """Instantiate a Google ADK Agent object."""
        try:
            from google.adk.agents import Agent
            return Agent(
                name=self.NAME,
                model=model,
                instruction=self.INSTRUCTIONS,
                tools=[evaluate_selectivity_ratios]
            )
        except (ImportError, Exception):
            return None
