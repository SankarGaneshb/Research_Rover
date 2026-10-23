"""Physicochemical & Binding Efficiency Agent."""

from typing import Tuple, Dict, Any, Optional
from ..models import CandidateInput, EfficiencyMetrics
from ..config import DEFAULT_TPP, TargetProductProfile
from ..tools.efficiency_tools import calculate_efficiency_metrics


class PhysChemAgent:
    """Agent responsible for Tier 1: Physicochemical profiling & efficiency metrics (LipE, LE, BEI)."""

    NAME = "PhysChem_Efficiency_Specialist"
    ROLE = "Physicochemical Properties and Ligand Efficiency Specialist"

    INSTRUCTIONS = (
        "You are an expert medicinal chemistry profiler specializing in physical properties and ligand efficiency. "
        "Your mission is to evaluate kinase inhibitors against the JAK2 Target Product Profile: "
        "ensure cLogP < 3.0 to avoid lipophilicity-driven toxicity, verify molecular weight < 450 Da, "
        "and enforce LipE >= 4.5 (ideal >= 5.5) and LE >= 0.32 (ideal >= 0.38). "
        "Flag any greasy modifications that attempt to achieve potency through non-specific hydrophobic bulk."
    )

    def __init__(self, tpp: TargetProductProfile = DEFAULT_TPP):
        self.tpp = tpp

    def analyze(self, candidate: CandidateInput) -> Tuple[EfficiencyMetrics, str]:
        """Perform deterministic efficiency calculations and scientific reasoning."""
        metrics = calculate_efficiency_metrics(
            jak2_ic50_nm=candidate.jak2_ic50_nm,
            clogp=candidate.clogp,
            heavy_atom_count=candidate.heavy_atom_count,
            mw=candidate.mw,
            tpp=self.tpp
        )

        reasoning_lines = [
            f"[{self.NAME}] Evaluation for candidate {candidate.candidate_id}:",
            f"- Lipophilic Ligand Efficiency (LipE): {metrics.lipe} (Target >= {self.tpp.lipe_acceptable_min}, Ideal >= {self.tpp.lipe_ideal_min})",
            f"- Ligand Efficiency (LE): {metrics.le} kcal/mol/HA (Target >= {self.tpp.le_acceptable_min})",
            f"- cLogP: {candidate.clogp} (Ideal <= {self.tpp.clogp_ideal_max})",
            f"- Molecular Weight: {candidate.mw} g/mol, TPSA: {candidate.tpsa} Å²"
        ]

        if candidate.clogp > self.tpp.clogp_ideal_max:
            reasoning_lines.append(
                f"  ⚠️ WARNING: cLogP exceeds ideal threshold of {self.tpp.clogp_ideal_max}. High risk of lipophilicity trap."
            )
        if not metrics.passes_efficiency_gate:
            reasoning_lines.append(
                "  ❌ GATE FAILED: Candidate does not meet minimum efficiency criteria (LipE/LE)."
            )
        else:
            reasoning_lines.append(
                "  ✅ GATE PASSED: Excellent binding efficiency per heavy atom and well-balanced lipophilicity."
            )

        return metrics, "\n".join(reasoning_lines)

    def create_adk_agent(self, model: str = "gemini-2.5-flash") -> Optional[Any]:
        """Instantiate a Google ADK Agent object if google-adk is available."""
        try:
            from google.adk.agents import Agent
            return Agent(
                name=self.NAME,
                model=model,
                instruction=self.INSTRUCTIONS,
                tools=[calculate_efficiency_metrics]
            )
        except (ImportError, Exception):
            return None
