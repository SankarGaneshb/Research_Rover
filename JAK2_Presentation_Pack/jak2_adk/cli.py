"""Command-line interface (CLI) for the JAK2 screening cascade orchestrator."""

import argparse
import json
import sys
from pathlib import Path
from typing import List

from .models import CandidateInput
from .workflow import JAK2ScreeningOrchestrator


def run_demo() -> None:
    """Run built-in benchmark candidates demonstrating the 3 key gate outcomes."""
    demo_candidates = [
        CandidateInput(
            candidate_id="JAK2-LEAD-001",
            smiles="Scaffold_Core_A",
            mw=412.5,
            clogp=2.3,
            tpsa=82.4,
            hbd=2,
            hba=5,
            rot_bonds=4,
            heavy_atom_count=30,
            jak2_ic50_nm=6.2,
            jak1_ic50_nm=280.0,
            jak3_ic50_nm=450.0,
            tyk2_ic50_nm=95.0,
            cellular_pstat5_ic50_nm=45.0,
            hlm_half_life_min=68.0,
            solubility_ug_ml=62.0,
            cyp3a4_ic50_um=24.0,
            cyp2d6_ic50_um=18.5,
            cyp2c9_ic50_um=15.0,
            herg_ic50_um=22.0,
            reactive_metabolite_risk=False,
            hepatotoxicity_alert=False,
            pains_alert=False
        ),
        CandidateInput(
            candidate_id="JAK2-GREASY-TRAP-002",
            smiles="Scaffold_Lipophilic_Bulk_B",
            mw=498.6,
            clogp=4.6,
            tpsa=58.2,
            hbd=1,
            hba=4,
            rot_bonds=7,
            heavy_atom_count=37,
            jak2_ic50_nm=4.1,
            jak1_ic50_nm=35.0,
            jak3_ic50_nm=52.0,
            tyk2_ic50_nm=18.0,
            cellular_pstat5_ic50_nm=180.0,
            hlm_half_life_min=14.0,
            solubility_ug_ml=6.5,
            cyp3a4_ic50_um=2.1,
            cyp2d6_ic50_um=3.8,
            cyp2c9_ic50_um=4.2,
            herg_ic50_um=3.4,
            reactive_metabolite_risk=False,
            hepatotoxicity_alert=False,
            pains_alert=False
        ),
        CandidateInput(
            candidate_id="JAK2-TOX-ALERT-003",
            smiles="Scaffold_Quinone_Precursor_C",
            mw=385.4,
            clogp=2.8,
            tpsa=88.5,
            hbd=2,
            hba=6,
            rot_bonds=4,
            heavy_atom_count=28,
            jak2_ic50_nm=12.0,
            jak1_ic50_nm=420.0,
            jak3_ic50_nm=680.0,
            tyk2_ic50_nm=140.0,
            cellular_pstat5_ic50_nm=78.0,
            hlm_half_life_min=42.0,
            solubility_ug_ml=38.0,
            cyp3a4_ic50_um=15.0,
            cyp2d6_ic50_um=12.0,
            cyp2c9_ic50_um=11.0,
            herg_ic50_um=18.0,
            reactive_metabolite_risk=True,
            hepatotoxicity_alert=True,
            pains_alert=False
        ),
    ]

    orchestrator = JAK2ScreeningOrchestrator()
    reports = orchestrator.evaluate_batch(demo_candidates)

    print("\n" + "=" * 70)
    print("JAK2 MULTI-AGENT SCREENING CASCADE & TPP EVALUATION (GOOGLE ADK)")
    print("=" * 70 + "\n")

    for r in reports:
        print(f"Candidate: {r.candidate_id:<24} | Verdict: {r.verdict.value:<26} | MPO: {r.composite_mpo:.3f}")
        print(f"  LipE: {r.efficiency.lipe} | LE: {r.efficiency.le} | DILI Tier: {r.toxicology.dili_risk_level}")
        if r.gate_failures:
            print(f"  Gate Flags: {'; '.join(r.gate_failures)}")
        print("-" * 70)

    # Print full dossier for the top candidate
    print("\n" + orchestrator.format_report_markdown(reports[0]))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="JAK2 Kinase Screening Cascade & TPP Governance CLI")
    parser.add_argument("--demo", action="store_true", help="Run benchmark demo candidates")
    parser.add_argument("--input", type=str, help="Path to input JSON file containing candidates")
    parser.add_argument("--output", type=str, help="Path to save evaluation results (JSON or Markdown)")
    parser.add_argument("--format", choices=["json", "md"], default="md", help="Output format (default: md)")
    parser.add_argument("--check-adk", action="store_true", help="Check Google ADK SequentialAgent initialization")

    args = parser.parse_args()

    orchestrator = JAK2ScreeningOrchestrator()

    if args.check_adk:
        adk_agent = orchestrator.build_adk_sequential_agent()
        if adk_agent:
            print(f"[OK] Successfully initialized Google ADK agent: {adk_agent.name}")
            print(f"     Sub-agents count: {len(adk_agent.sub_agents)}")
            for sub in adk_agent.sub_agents:
                print(f"     - Sub-agent: {sub.name}")
        else:
            print("[WARN] Google ADK SequentialAgent could not be initialized.")
        return

    if args.demo or not args.input:
        run_demo()
        return

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {args.input} does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        candidates = [CandidateInput(**data)]
    elif isinstance(data, list):
        candidates = [CandidateInput(**item) for item in data]
    else:
        print("Error: Input must be a JSON object or array of objects.", file=sys.stderr)
        sys.exit(1)

    reports = orchestrator.evaluate_batch(candidates)

    if args.output:
        out_path = Path(args.output)
        if args.format == "json":
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump([r.model_dump() for r in reports], f, indent=2)
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                for r in reports:
                    f.write(orchestrator.format_report_markdown(r) + "\n\n---\n\n")
        print(f"Results successfully saved to {out_path}")
    else:
        for r in reports:
            print(orchestrator.format_report_markdown(r))
            print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
