# JAK2 Kinase Inhibitor TPP & Multi-Agent Screening Cascade (Google ADK)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK 2.12+](https://img.shields.io/badge/Google%20ADK-2.12+-4285F4.svg)](https://adk.dev)
[![Tests Passing](https://img.shields.io/badge/tests-12%20passed-success.svg)](tests/)

An automated, multi-agent Target Product Profile (TPP) and Screening Cascade system for optimizing a **JAK2 kinase inhibitor** hit molecule. Built natively on **Google Agent Development Kit (`google-adk`)**, the system coordinates specialized AI agents and deterministic calculation engines to triage candidate molecules across physicochemical fit, kinase selectivity, in vitro ADMET, and drug-induced liver injury (DILI) avoidance.

---

## Table of Contents
1. [Executive Summary for Leadership](#executive-summary-for-leadership)
2. [Quick Start (3-Minute Setup)](#quick-start-3-minute-setup)
3. [System Architecture](#system-architecture)
4. [Target Product Profile (TPP) Configuration](#target-product-profile-tpp-configuration)
5. [How Research Associates Can Modify Thresholds](#how-research-associates-can-modify-thresholds)
6. [How IT Teams Can Deploy and Integrate](#how-it-teams-can-deploy-and-integrate)
7. [Running Tests and Verification](#running-tests-and-verification)
8. [Generating Presentation Packs for Management](#generating-presentation-packs-for-management)

---

## Executive Summary for Leadership

Early drug discovery campaigns often fail because molecules with high test-tube potency turn out to be greasy, non-selective, or toxic to liver cells. This system prevents wasted in vivo animal testing by applying a **Four-Tier Stage-Gate Funnel**:

```
[100 Hit Molecules]
         │
         ▼ Tier 1: PhysChem & Efficiency (Filters out greasy/insoluble compounds)
  [38 Molecules]
         │
         ▼ Tier 2: Kinome Selectivity (Filters out pan-JAK immunosuppressive hits)
  [14 Molecules]
         │
         ▼ Tier 3: Liver & ADMET Safety (Filters out reactive metabolites & CYP liabilities)
   [4 Molecules]
         │
         ▼ Tier 4: Multi-Parameter Optimization (MPO >= 0.75)
   [1 Winner] ──> Advance to Animal In Vivo Studies (~$1.2M+ saved in failed trials)
```

---

## Quick Start (3-Minute Setup)

### 1. Prerequisites
* Python 3.10 to 3.13 installed.
* PowerShell or standard Bash terminal.

### 2. Environment Activation
```powershell
# Navigate to project
cd C:\Users\bsank\Research_Rover

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

### 3. Run Benchmark Demo
```powershell
python -m jak2_adk.cli --demo
```

### 4. Verify Google ADK Agent Orchestration
```powershell
python -m jak2_adk.cli --check-adk
```

### 5. Screen Custom Molecules (Batch Mode)
```powershell
python -m jak2_adk.cli --input examples/candidates.json --output results.md --format md
```

---

## System Architecture

The pipeline pairs deterministic biophysical tools with **Google ADK Agents** arranged in a `SequentialAgent` workflow:

```
                          Candidate Data (JSON / Assay DB)
                                        │
                                        ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │         Google ADK Orchestrator (JAK2ScreeningOrchestrator)            │
   └───────┬───────────────────┬───────────────────┬────────────────────┬───┘
           │                   │                   │                    │
           ▼                   ▼                   ▼                    ▼
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐    ┌───────────────┐
   │ PhysChemAgent │   │  KinaseAgent  │   │   ToxAgent    │    │GovernanceAgent│
   │               │   │               │   │               │    │               │
   │ • cLogP < 3.0 │   │ • JAK2 < 10nM │   │ • Zero DILI   │    │ • MPO Desir-  │
   │ • LipE >= 5.0 │   │ • JAK1 > 30x  │   │ • No GSH trap │    │   ability     │
   │ • LE >= 0.35  │   │ • JAK3 > 50x  │   │ • CYP clean   │    │ • Gate Veto   │
   └───────────────┘   └───────────────┘   └───────────────┘    └───────────────┘
```

---

## Target Product Profile (TPP) Configuration

All screening limits are declaratively maintained in `jak2_adk/config.py`:

| Pillar | Metric | Acceptable Gate | Ideal Goal | MPO Weight |
| :--- | :--- | :--- | :--- | :--- |
| **Potency** | JAK2 Enzymatic $\text{IC}_{50}$<br>Cellular $\text{pSTAT5 IC}_{50}$ | $< 50\text{ nM}$<br>$< 250\text{ nM}$ | $< 10\text{ nM}$<br>$< 100\text{ nM}$ | **35%** |
| **Selectivity** | vs. JAK1<br>vs. JAK3<br>vs. TYK2 | $\ge 30\times$<br>$\ge 50\times$<br>$\ge 10\times$ | $\ge 50\times$<br>$\ge 100\times$<br>$\ge 20\times$ | **20%** |
| **Safety & DILI** | Reactive Metabolite (GSH)<br>Core Hepatotoxicity<br>CYP Inhibition ($3\text{A}4, 2\text{D}6, 2\text{C}9$)<br>hERG Cardiotoxicity | Clean<br>Clean<br>$\text{IC}_{50} \ge 10\text{ }\mu\text{M}$<br>$\text{IC}_{50} \ge 10\text{ }\mu\text{M}$ | No flags<br>No flags<br>$\ge 30\text{ }\mu\text{M}$<br>$\ge 30\text{ }\mu\text{M}$ | **25%** |
| **PhysChem & LipE** | $\text{cLog}P$<br>$\text{LipE}$ ($\text{pIC}_{50} - \text{cLog}P$)<br>$\text{LE}$ ($\text{kcal/mol/HA}$) | $\le 3.5$<br>$\ge 4.5$<br>$\ge 0.32$ | $\le 3.0$<br>$\ge 5.5$<br>$\ge 0.38$ | **10%** |
| **Developability** | Thermodynamic Solubility<br>Microsomal Half-Life ($T_{1/2}$) | $\ge 20\text{ }\mu\text{g/mL}$<br>$\ge 30\text{ min}$ | $\ge 50\text{ }\mu\text{g/mL}$<br>$\ge 60\text{ min}$ | **10%** |

---

## Team Guides & Documentation Links

* [Research Associate Guide](docs/RESEARCH_ASSOCIATE_GUIDE.md): Practical guide on adding molecules, modifying TPP criteria, and generating executive slides.
* [IT & Deployment Guide](docs/IT_DEPLOYMENT_GUIDE.md): Technical guide for database integration, Docker containerization, and Cloud Run deployment.
* [System Architecture](docs/ARCHITECTURE.md): Mathematical derivations of MPO desirability and Google ADK agent specifications.

---

## Presentation Pack for Senior Management

To regenerate visual assets and update the self-contained briefing pack:
```powershell
python generate_visualizations.py
python package_share.py
```
* **Interactive Briefing**: Double-click `Executive_JAK2_Report.html` (opens in any browser with zero setup).
* **Shareable Archive**: `JAK2_Presentation_Pack.zip` (bundles HTML report, high-res PNG charts, and Python code).
