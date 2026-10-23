# System Architecture & Biophysical Foundations

This document details the architectural decisions, biophysical models, and scoring mechanics powering the JAK2 multi-agent optimization pipeline.

---

## 1. High-Level Architecture

The system bridges **Google Agent Development Kit (`google-adk`)** with deterministic biophysical calculators:

```
                            Input Layer
                   (Candidate Assay Data / JSON)
                                │
                                ▼
                   Google ADK Workflow Runtime
         ┌───────────────────────────────────────────────┐
         │     JAK2ScreeningOrchestrator                 │
         │     SequentialAgent Graph Execution           │
         └───────┬──────────────┬──────────────┬─────────┘
                 │              │              │
                 ▼              ▼              ▼
           Tier 1 Agent   Tier 2 Agent   Tier 3 Agent
           (PhysChem)     (Kinase)       (Toxicology)
                 │              │              │
                 └──────────────┼──────────────┘
                                │
                                ▼
                          Tier 4 Agent
                          (Governance)
                                │
                                ▼
                       Harrington-Derringer
                         MPO Desirability
                                │
                                ▼
                        Gate Verdict:
                ADVANCE / HOLD / REJECT + Dossier
```

---

## 2. Multi-Parameter Optimization (MPO) Desirability Math

Rather than binary step functions that discard promising compounds on borderline metrics, the system implements continuous **Harrington / Derringer Desirability Functions** ($d_i \in [0.0, 1.0]$):

### A. Linear Ramping Functions:
* **Lower is Better** (e.g., $\text{IC}_{50}$, $\text{cLog}P$):
  $$d(x) = \begin{cases} 
  1.0 & x \le x_{\text{ideal}} \\
  \frac{x_{\text{acceptable}} - x}{x_{\text{acceptable}} - x_{\text{ideal}}} & x_{\text{ideal}} < x < x_{\text{acceptable}} \\
  0.0 & x \ge x_{\text{acceptable}}
  \end{cases}$$

* **Higher is Better** (e.g., $\text{LipE}$, $\text{LE}$, Fold Selectivity, Solubility):
  $$d(x) = \begin{cases} 
  0.0 & x \le x_{\text{acceptable}} \\
  \frac{x - x_{\text{acceptable}}}{x_{\text{ideal}} - x_{\text{acceptable}}} & x_{\text{acceptable}} < x < x_{\text{ideal}} \\
  1.0 & x \ge x_{\text{ideal}}
  \end{cases}$$

### B. Weighted Composite Desirability:
$$D_{\text{composite}} = \sum_{k=1}^{5} w_k \cdot S_k$$
where:
* $S_{\text{potency}} \times 0.35$
* $S_{\text{selectivity}} \times 0.20$
* $S_{\text{safety\_dili}} \times 0.25$
* $S_{\text{physchem}} \times 0.10$
* $S_{\text{developability}} \times 0.10$
$$\sum w_k = 1.00$$

---

## 3. The 3 Diagnostic Benchmark Profiles

To validate that the pipeline distinguishes good molecules from toxic or greasy traps, three benchmark profiles are maintained in `examples/candidates.json`:

### 1. `JAK2-LEAD-001` (The Ideal Lead)
* $\text{JAK2 IC}_{50} = 6.2\text{ nM}$, cellular $\text{pSTAT5} = 45\text{ nM}$.
* $\text{cLog}P = 2.3$, $\text{LipE} = 5.91$, $\text{LE} = 0.375\text{ kcal/mol/HA}$.
* $45\times$ selective over JAK1, $73\times$ over JAK3.
* Clean liver profile, zero reactive metabolites.
* **Result:** `ADVANCE_TO_IN_VIVO` ($\text{MPO} = 0.998$).

### 2. `JAK2-GREASY-TRAP-002` (The Lipophilicity Trap)
* $\text{JAK2 IC}_{50} = 4.1\text{ nM}$ in biochemical assays.
* $\text{cLog}P = 4.6$ (Extreme grease), $\text{LipE} = 3.79$ (Below bar).
* Broad pan-JAK activity (only $8.5\times$ over JAK1 $\rightarrow$ Immunosuppression).
* Insoluble ($6.5\text{ }\mu\text{g/mL}$), inhibits CYP3A4 ($2.1\text{ }\mu\text{M}$), blocks hERG ($3.4\text{ }\mu\text{M}$).
* **Result:** `REJECT_CRITICAL_LIABILITY` ($\text{MPO} = 0.407$).

### 3. `JAK2-TOX-ALERT-003` (The Hidden Poison Pill)
* $\text{JAK2 IC}_{50} = 12.0\text{ nM}$, $35\times\text{--}56\times$ selectivity.
* $\text{cLog}P = 2.8$, $\text{LipE} = 5.12$ (Passes physical gates).
* **Fatal Liability:** Forms reactive quinone-imine adducts that trigger severe Drug-Induced Liver Injury (DILI).
* **Result:** `REJECT_CRITICAL_LIABILITY` (Automatic Safety Veto despite $\text{MPO} = 0.780$).
