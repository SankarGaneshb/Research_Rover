"""Google ADK Multi-Agent Workflow Orchestrator for the JAK2 Screening Cascade."""

from typing import Optional, Dict, Any, List
from .models import CandidateInput, CandidateEvaluationReport, DecisionVerdict
from .config import DEFAULT_TPP, TargetProductProfile
from .agents import PhysChemAgent, KinaseAgent, ToxAgent, GovernanceAgent


class JAK2ScreeningOrchestrator:
    """Orchestrator for the JAK2 kinase inhibitor screening cascade and decision gates."""

    def __init__(self, tpp: TargetProductProfile = DEFAULT_TPP, model: str = "gemini-2.5-flash"):
        self.tpp = tpp
        self.model = model
        self.physchem_agent = PhysChemAgent(tpp=tpp)
        self.kinase_agent = KinaseAgent(tpp=tpp)
        self.tox_agent = ToxAgent(tpp=tpp)
        self.governance_agent = GovernanceAgent(tpp=tpp)

    def build_adk_sequential_agent(self) -> Optional[Any]:
        """Construct a native Google ADK SequentialAgent coordinating all specialized agents."""
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                from google.adk.agents import SequentialAgent
                sub_agents = []
                for agent_instance in [self.physchem_agent, self.kinase_agent, self.tox_agent, self.governance_agent]:
                    adk_sub = agent_instance.create_adk_agent(model=self.model)
                    if adk_sub:
                        sub_agents.append(adk_sub)

                if not sub_agents:
                    return None

                return SequentialAgent(
                    name="JAK2_Optimization_Cascade_Orchestrator",
                    description="Google ADK sequential multi-agent screening cascade for JAK2 kinase inhibitors",
                    sub_agents=sub_agents
                )
        except (ImportError, Exception):
            return None

    def evaluate_candidate(self, candidate: CandidateInput) -> CandidateEvaluationReport:
        """Execute the multi-tier screening cascade on a candidate molecule."""
        agent_reasoning: Dict[str, str] = {}

        # Tier 1: PhysChem & Efficiency
        efficiency_metrics, physchem_notes = self.physchem_agent.analyze(candidate)
        agent_reasoning["PhysChem_Specialist"] = physchem_notes

        # Tier 2: Potency & Isoform Selectivity
        selectivity_metrics, kinase_notes = self.kinase_agent.analyze(candidate)
        agent_reasoning["Kinase_Specialist"] = kinase_notes

        # Tier 3: In Vitro ADMET, DILI & Safety
        tox_evaluation, tox_notes = self.tox_agent.analyze(candidate)
        agent_reasoning["Toxicology_Specialist"] = tox_notes

        # Tier 4: Portfolio Governance & MPO Decision Gate
        report = self.governance_agent.synthesize(
            candidate=candidate,
            efficiency=efficiency_metrics,
            selectivity=selectivity_metrics,
            toxicology=tox_evaluation,
            agent_reasoning=agent_reasoning
        )

        return report

    def evaluate_batch(self, candidates: List[CandidateInput]) -> List[CandidateEvaluationReport]:
        """Evaluate a batch of candidate molecules across the screening cascade."""
        return [self.evaluate_candidate(c) for c in candidates]

    @staticmethod
    def format_report_markdown(report: CandidateEvaluationReport) -> str:
        """Format an evaluation report as GitHub-flavored Markdown."""
        verdict_badge = {
            DecisionVerdict.ADVANCE: "[ADVANCE TO IN VIVO]",
            DecisionVerdict.HOLD: "[HOLD FOR OPTIMIZATION]",
            DecisionVerdict.REJECT: "[REJECT / CRITICAL LIABILITY]"
        }.get(report.verdict, report.verdict.value)

        lines = [
            f"# Screening Dossier: Candidate `{report.candidate_id}`",
            f"**Decision Gate Verdict:** {verdict_badge}",
            f"**Composite MPO Score:** `{report.composite_mpo:.3f} / 1.000`",
            "",
            "## 1. Multi-Parameter Optimization (MPO) Pillar Scores",
            "| Pillar | Weight | Pillar Score | Key Driver |",
            "| :--- | :--- | :--- | :--- |",
            f"| Potency | 35% | `{report.mpo_scores.potency_score:.3f}` | JAK2 IC50 & cellular pSTAT5 |",
            f"| Selectivity | 20% | `{report.mpo_scores.selectivity_score:.3f}` | JAK1/3 & TYK2 selectivity window |",
            f"| Safety & DILI | 25% | `{report.mpo_scores.safety_dili_score:.3f}` | Reactive metabolites & CYP profile |",
            f"| PhysChem & LipE | 10% | `{report.mpo_scores.physchem_score:.3f}` | cLogP, LipE & Ligand Efficiency |",
            f"| Developability | 10% | `{report.mpo_scores.developability_score:.3f}` | Solubility & microsomal stability |",
            "",
            "## 2. Key Calculated Properties",
            f"- **Lipophilic Ligand Efficiency (LipE):** `{report.efficiency.lipe}`",
            f"- **Ligand Efficiency (LE):** `{report.efficiency.le}` kcal/mol/HA",
            f"- **Binding Efficiency Index (BEI):** `{report.efficiency.bei}`",
            f"- **Selectivity Window:** `{report.selectivity.selectivity_summary}`",
            f"- **DILI Risk Assessment:** `{report.toxicology.dili_risk_level}`",
            ""
        ]

        if report.gate_failures:
            lines.extend([
                "## 3. Critical Gate Liabilities",
                *[f"- ⚠️ {failure}" for failure in report.gate_failures],
                ""
            ])

        lines.extend([
            "## 4. Multi-Agent Reasoning Dossier",
            f"### Physicochemical & Efficiency Specialist\n```\n{report.agent_reasoning.get('PhysChem_Specialist', '')}\n```\n",
            f"### Kinase Potency & Selectivity Specialist\n```\n{report.agent_reasoning.get('Kinase_Specialist', '')}\n```\n",
            f"### Toxicology & Safety Specialist\n```\n{report.agent_reasoning.get('Toxicology_Specialist', '')}\n```\n",
            f"### Portfolio Governance Lead\n```\n{report.agent_reasoning.get('Governance', '')}\n```\n"
        ])

        return "\n".join(lines)
