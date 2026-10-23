# Research Associate Guide: JAK2 Kinase Optimizer

This guide is written for Research Associates, Computational Chemists, and Biophysicists running or adapting the JAK2 screening cascade.

---

## 1. How the Four-Tier Cascade Works

1. **Tier 1: Physicochemical Fit & Ligand Efficiency (`PhysChemAgent`)**:
   * Evaluates molecular weight, topological polar surface area ($\text{TPSA}$), and calculated lipophilicity ($\text{cLog}P$).
   * Computes **$\text{LipE} = \text{pIC}_{50} - \text{cLog}P$** and **$\text{LE} = 1.37 \times \text{pIC}_{50} / \text{HAC}$**.
   * Flags "greasy traps" where affinity increases purely by adding non-specific hydrophobic groups.

2. **Tier 2: Target Potency & Kinome Selectivity (`KinaseAgent`)**:
   * Measures target engagement: JAK2 biochemical $\text{IC}_{50} < 10\text{ nM}$ (Ideal) / $< 50\text{ nM}$ (Acceptable).
   * Measures cellular target engagement: $\text{pSTAT5 IC}_{50} < 100\text{ nM}$.
   * Enforces isoform selectivity: $\ge 30\times$ vs JAK1, $\ge 50\times$ vs JAK3, $\ge 10\times$ vs TYK2 to prevent pan-JAK immunosuppressive liabilities.

3. **Tier 3: In Vitro ADMET & Liver Safety (`ToxAgent`)**:
   * Evaluates **Drug-Induced Liver Injury (DILI)** risks: Rule-of-Two ($\text{cLog}P > 3.0$), GSH adducts (reactive metabolites), and HepG2 cytotoxicity flags.
   * Assesses CYP enzyme inhibition ($3\text{A}4, 2\text{D}6, 2\text{C}9 \ge 10\text{ }\mu\text{M}$ required).
   * Checks cardiac liability ($\text{hERG} \ge 10\text{ }\mu\text{M}$) and metabolic turnover ($\text{HLM } T_{1/2} \ge 30\text{ min}$).

4. **Tier 4: Portfolio Governance & Decision Gates (`GovernanceAgent`)**:
   * Combines all pillars into a continuous composite **Multi-Parameter Optimization (MPO)** desirability score between $0.000$ and $1.000$.
   * Issues final gate verdicts:
     * `ADVANCE_TO_IN_VIVO` ($\text{MPO} \ge 0.75$, zero critical flags)
     * `HOLD_FOR_OPTIMIZATION` ($0.50 \le \text{MPO} < 0.75$, fixable liabilities)
     * `REJECT_CRITICAL_LIABILITY` ($\text{MPO} < 0.50$ or fatal safety veto)

---

## 2. Adding New Compounds to the Evaluation Queue

Create or edit a JSON file (e.g. `examples/my_series.json`):

```json
[
  {
    "candidate_id": "SERIES-004",
    "smiles": "Scaffold_Series_4",
    "mw": 415.2,
    "clogp": 2.35,
    "tpsa": 81.0,
    "hbd": 2,
    "hba": 5,
    "rot_bonds": 4,
    "heavy_atom_count": 30,
    "jak2_ic50_nm": 6.5,
    "jak1_ic50_nm": 290.0,
    "jak3_ic50_nm": 480.0,
    "tyk2_ic50_nm": 110.0,
    "cellular_pstat5_ic50_nm": 46.0,
    "hlm_half_life_min": 65.0,
    "solubility_ug_ml": 56.0,
    "cyp3a4_ic50_um": 22.0,
    "cyp2d6_ic50_um": 18.0,
    "cyp2c9_ic50_um": 15.0,
    "herg_ic50_um": 20.0,
    "reactive_metabolite_risk": false,
    "hepatotoxicity_alert": false,
    "pains_alert": false
  }
]
```

Run evaluation:
```powershell
python -m jak2_adk.cli --input examples/my_series.json --output series_report.md
```

---

## 3. How to Modify TPP Parameters in `config.py`

All limits and weights are centralized in `jak2_adk/config.py`.

### Scenario A: Management requests a stricter JAK1 selectivity window (50x instead of 30x)
```python
# In jak2_adk/config.py
@dataclass(frozen=True)
class TargetProductProfile:
    selectivity_jak1_fold_min: float = 50.0  # Changed from 30.0
```

### Scenario B: Shifting from Oncology (MPN) to Autoimmune / Inflammatory
In autoimmune indications, dual JAK1/JAK2 inhibition might be tolerated or desired, but cardiac and liver safety bars are even higher:
```python
# In jak2_adk/config.py
@dataclass(frozen=True)
class TargetProductProfile:
    selectivity_jak1_fold_min: float = 5.0   # Relaxed for dual profile
    cyp_inhibition_ic50_min_um: float = 20.0 # Stricter CYP window
    herg_ic50_min_um: float = 20.0           # Stricter hERG window
```

### Scenario C: Re-weighting the Five Pillars
```python
# In jak2_adk/config.py
    weights: Dict[str, float] = field(default_factory=lambda: {
        "potency": 0.25,        # 25% Potency
        "selectivity": 0.25,    # 25% Selectivity
        "safety_dili": 0.35,    # 35% Heavily prioritize liver safety
        "physchem": 0.10,       # 10% PhysChem
        "developability": 0.05  # 5% Developability
    })
```

---

## 4. Re-Generating Management Presentation Assets

When you update data or thresholds, regenerate the visual slides and shareable packages:

```powershell
# 1. Regenerate the 4 visual figures (Radar, Sweetspot, Selectivity, Funnel)
python generate_visualizations.py

# 2. Rebuild the standalone Executive_JAK2_Report.html and JAK2_Presentation_Pack.zip
python package_share.py
```
* **To present interactively**: Open `Executive_JAK2_Report.html` in Chrome/Edge/Safari.
* **To paste into PowerPoint**: Copy PNG files from `JAK2_Presentation_Pack.zip` (`visual_charts/`).
