"""Decision Gate & Multi-Parameter Optimization (MPO) Governance Agent."""

from typing import Tuple, List, Optional, Any
from ..models import CandidateInput, EfficiencyMetrics, SelectivityMetrics, ToxicologyEvaluation, MPOScores, DecisionVerdict, CandidateEvaluationReport
from ..config import DEFAULT_TPP, TargetProductProfile
from ..tools.mpo_tools import compute_mpo_score


class GovernanceAgent:
    """Agent responsible for Tier 4: MPO Desirability synthesis and Go/No-Go Decision Gate Governance."""

    NAME = "MPO_Governance_Decision_Specialist"
    ROLE = "Portfolio Governance and Decision Gate Lead"

    INSTRUCTIONS = (
        "You are the project director and portfolio governance lead for the JAK2 medicinal chemistry campaign. "
        "Your mission is to weigh multi-parameter optimization (MPO) desirability across: "
        "Potency (35%), Selectivity (20%), Safety/DILI (25%), PhysChem (10%), and Developability (10%). "
        "Enforce strict decision gates: Advance only compounds with MPO >= 0.75 and zero critical alerts. "
        "Reject compounds with severe reactive liabilities or lipophilicity traps. Issue clear rationale for team next steps."
    )

    def __init__(self, tpp: TargetProductProfile = DEFAULT_TPP):
        self.tpp = tpp

    def synthesize(
        self,
        candidate: CandidateInput,
        efficiency: EfficiencyMetrics,
        selectivity: SelectivityMetrics,
        toxicology: ToxicologyEvaluation,
        agent_reasoning: dict
    ) -> CandidateEvaluationReport:
        """Calculate composite MPO scores, apply gates, and assemble the final dossier."""
        mpo_scores, verdict, gate_failures = compute_mpo_score(
            candidate=candidate,
            efficiency=efficiency,
            selectivity=selectivity,
            toxicology=toxicology,
            tpp=self.tpp
        )

        reasoning_lines = [
            f"[{self.NAME}] Synthesis for candidate {candidate.candidate_id}:",
            f"- Composite MPO Score: {mpo_scores.composite_mpo:.3f} / 1.000 (Advance Threshold: >= {self.tpp.mpo_advance_threshold})",
            f"  * Potency Pillar (35%): {mpo_scores.potency_score:.3f}",
            f"  * Selectivity Pillar (20%): {mpo_scores.selectivity_score:.3f}",
            f"  * Safety & DILI Pillar (25%): {mpo_scores.safety_dili_score:.3f}",
            f"  * PhysChem & LipE Pillar (10%): {mpo_scores.physchem_score:.3f}",
            f"  * Developability Pillar (10%): {mpo_scores.developability_score:.3f}",
            f"- Final Decision Gate Verdict: {verdict.value}"
        ]

        if gate_failures:
            reasoning_lines.append("  ⚠️ GATE OBSTACLES IDENTIFIED:")
            for failure in gate_failures:
                reasoning_lines.append(f"    * {failure}")

        agent_reasoning["Governance"] = "\n".join(reasoning_lines)

        return CandidateEvaluationReport(
            candidate_id=candidate.candidate_id,
            verdict=verdict,
            composite_mpo=mpo_scores.composite_mpo,
            efficiency=efficiency,
            selectivity=selectivity,
            toxicology=toxicology,
            mpo_scores=mpo_scores,
            gate_failures=gate_failures,
            agent_reasoning=agent_reasoning
        )

    def create_adk_agent(self, model: str = "gemini-2.5-flash") -> Optional[Any]:
        """Instantiate a Google ADK Agent object."""
        try:
            from google.adk.agents import Agent
            return Agent(
                name=self.NAME,
                model=model,
                instruction=self.INSTRUCTIONS,
                tools=[compute_mpo_score]
            )
        except (ImportError, Exception):
            return None
