# Screening Dossier: Candidate `JAK2-LEAD-001`
**Decision Gate Verdict:** [ADVANCE TO IN VIVO]
**Composite MPO Score:** `0.998 / 1.000`

## 1. Multi-Parameter Optimization (MPO) Pillar Scores
| Pillar | Weight | Pillar Score | Key Driver |
| :--- | :--- | :--- | :--- |
| Potency | 35% | `1.000` | JAK2 IC50 & cellular pSTAT5 |
| Selectivity | 20% | `1.000` | JAK1/3 & TYK2 selectivity window |
| Safety & DILI | 25% | `1.000` | Reactive metabolites & CYP profile |
| PhysChem & LipE | 10% | `0.983` | cLogP, LipE & Ligand Efficiency |
| Developability | 10% | `1.000` | Solubility & microsomal stability |

## 2. Key Calculated Properties
- **Lipophilic Ligand Efficiency (LipE):** `5.91`
- **Ligand Efficiency (LE):** `0.375` kcal/mol/HA
- **Binding Efficiency Index (BEI):** `19.9`
- **Selectivity Window:** `JAK1: 45.2x (>= 30.0x) | JAK3: 72.6x (>= 50.0x) | TYK2: 15.3x (>= 10.0x)`
- **DILI Risk Assessment:** `LOW`

## 4. Multi-Agent Reasoning Dossier
### Physicochemical & Efficiency Specialist
```
[PhysChem_Efficiency_Specialist] Evaluation for candidate JAK2-LEAD-001:
- Lipophilic Ligand Efficiency (LipE): 5.91 (Target >= 4.5, Ideal >= 5.5)
- Ligand Efficiency (LE): 0.375 kcal/mol/HA (Target >= 0.32)
- cLogP: 2.3 (Ideal <= 3.0)
- Molecular Weight: 412.5 g/mol, TPSA: 82.4 Å²
  ✅ GATE PASSED: Excellent binding efficiency per heavy atom and well-balanced lipophilicity.
```

### Kinase Potency & Selectivity Specialist
```
[Kinase_Potency_Selectivity_Specialist] Evaluation for candidate JAK2-LEAD-001:
- JAK2 Enzymatic IC50: 6.2 nM (Target <= 50.0 nM)
- Cellular pSTAT5 IC50: 45.0 nM (Target <= 250.0 nM)
- Isoform Selectivity Folds: JAK1: 45.2x (>= 30.0x) | JAK3: 72.6x (>= 50.0x) | TYK2: 15.3x (>= 10.0x)
  ✅ SELECTIVITY GATE PASSED: Clean selectivity window sparing JAK1, JAK3, and TYK2.
```

### Toxicology & Safety Specialist
```
[ADMET_DILI_Safety_Specialist] Safety evaluation for candidate JAK2-LEAD-001:
- DILI Risk Tier: LOW
- Metabolic Stability: HLM T1/2 68.0 min (Target >= 30.0 min)
- CYP Inhibition Status: Clean
- hERG Status: Clean (IC50 22.0 µM)
  ✅ SAFETY PROFILE CLEAN: No critical structural or metabolic flags.
```

### Portfolio Governance Lead
```
[MPO_Governance_Decision_Specialist] Synthesis for candidate JAK2-LEAD-001:
- Composite MPO Score: 0.998 / 1.000 (Advance Threshold: >= 0.75)
  * Potency Pillar (35%): 1.000
  * Selectivity Pillar (20%): 1.000
  * Safety & DILI Pillar (25%): 1.000
  * PhysChem & LipE Pillar (10%): 0.983
  * Developability Pillar (10%): 1.000
- Final Decision Gate Verdict: ADVANCE_TO_IN_VIVO
```


---

# Screening Dossier: Candidate `JAK2-GREASY-TRAP-002`
**Decision Gate Verdict:** [REJECT / CRITICAL LIABILITY]
**Composite MPO Score:** `0.407 / 1.000`

## 1. Multi-Parameter Optimization (MPO) Pillar Scores
| Pillar | Weight | Pillar Score | Key Driver |
| :--- | :--- | :--- | :--- |
| Potency | 35% | `0.733` | JAK2 IC50 & cellular pSTAT5 |
| Selectivity | 20% | `0.275` | JAK1/3 & TYK2 selectivity window |
| Safety & DILI | 25% | `0.380` | Reactive metabolites & CYP profile |
| PhysChem & LipE | 10% | `0.006` | cLogP, LipE & Ligand Efficiency |
| Developability | 10% | `0.000` | Solubility & microsomal stability |

## 2. Key Calculated Properties
- **Lipophilic Ligand Efficiency (LipE):** `3.79`
- **Ligand Efficiency (LE):** `0.311` kcal/mol/HA
- **Binding Efficiency Index (BEI):** `16.82`
- **Selectivity Window:** `JAK1 FAIL: 8.5x (< 30.0x) | JAK3 FAIL: 12.7x (< 50.0x) | TYK2 FAIL: 4.4x (< 10.0x)`
- **DILI Risk Assessment:** `HIGH`

## 3. Critical Gate Liabilities
- ⚠️ Selectivity Gate: Insufficient window (JAK1 FAIL: 8.5x (< 30.0x) | JAK3 FAIL: 12.7x (< 50.0x) | TYK2 FAIL: 4.4x (< 10.0x))
- ⚠️ PhysChem Gate: Lipophilicity trap cLogP 4.6 > 3.5

## 4. Multi-Agent Reasoning Dossier
### Physicochemical & Efficiency Specialist
```
[PhysChem_Efficiency_Specialist] Evaluation for candidate JAK2-GREASY-TRAP-002:
- Lipophilic Ligand Efficiency (LipE): 3.79 (Target >= 4.5, Ideal >= 5.5)
- Ligand Efficiency (LE): 0.311 kcal/mol/HA (Target >= 0.32)
- cLogP: 4.6 (Ideal <= 3.0)
- Molecular Weight: 498.6 g/mol, TPSA: 58.2 Å²
  ⚠️ WARNING: cLogP exceeds ideal threshold of 3.0. High risk of lipophilicity trap.
  ❌ GATE FAILED: Candidate does not meet minimum efficiency criteria (LipE/LE).
```

### Kinase Potency & Selectivity Specialist
```
[Kinase_Potency_Selectivity_Specialist] Evaluation for candidate JAK2-GREASY-TRAP-002:
- JAK2 Enzymatic IC50: 4.1 nM (Target <= 50.0 nM)
- Cellular pSTAT5 IC50: 180.0 nM (Target <= 250.0 nM)
- Isoform Selectivity Folds: JAK1 FAIL: 8.5x (< 30.0x) | JAK3 FAIL: 12.7x (< 50.0x) | TYK2 FAIL: 4.4x (< 10.0x)
  ❌ SELECTIVITY GATE FAILED: Inadequate margin against off-target JAK isoforms; risk of pan-JAK immunosuppression.
```

### Toxicology & Safety Specialist
```
[ADMET_DILI_Safety_Specialist] Safety evaluation for candidate JAK2-GREASY-TRAP-002:
- DILI Risk Tier: HIGH
- Metabolic Stability: HLM T1/2 14.0 min (Target >= 30.0 min)
- CYP Inhibition Status: FLAGGED
- hERG Status: FLAGGED (IC50 3.4 µM)
  ⚠️ IDENTIFIED SAFETY LIABILITIES:
    * Rule-of-Two DILI Risk: cLogP 4.60 > 3.0
    * CYP3A4 Liability: IC50 2.1 µM < 10.0 µM
    * CYP2D6 Liability: IC50 3.8 µM < 10.0 µM
    * CYP2C9 Liability: IC50 4.2 µM < 10.0 µM
    * Metabolic Clearance Liability: HLM T1/2 14.0 min < 30.0 min
    * hERG Cardiotoxicity Alert: IC50 3.4 µM < 10.0 µM
```

### Portfolio Governance Lead
```
[MPO_Governance_Decision_Specialist] Synthesis for candidate JAK2-GREASY-TRAP-002:
- Composite MPO Score: 0.407 / 1.000 (Advance Threshold: >= 0.75)
  * Potency Pillar (35%): 0.733
  * Selectivity Pillar (20%): 0.275
  * Safety & DILI Pillar (25%): 0.380
  * PhysChem & LipE Pillar (10%): 0.006
  * Developability Pillar (10%): 0.000
- Final Decision Gate Verdict: REJECT_CRITICAL_LIABILITY
  ⚠️ GATE OBSTACLES IDENTIFIED:
    * Selectivity Gate: Insufficient window (JAK1 FAIL: 8.5x (< 30.0x) | JAK3 FAIL: 12.7x (< 50.0x) | TYK2 FAIL: 4.4x (< 10.0x))
    * PhysChem Gate: Lipophilicity trap cLogP 4.6 > 3.5
```


---

# Screening Dossier: Candidate `JAK2-TOX-ALERT-003`
**Decision Gate Verdict:** [REJECT / CRITICAL LIABILITY]
**Composite MPO Score:** `0.780 / 1.000`

## 1. Multi-Parameter Optimization (MPO) Pillar Scores
| Pillar | Weight | Pillar Score | Key Driver |
| :--- | :--- | :--- | :--- |
| Potency | 35% | `0.975` | JAK2 IC50 & cellular pSTAT5 |
| Selectivity | 20% | `1.000` | JAK1/3 & TYK2 selectivity window |
| Safety & DILI | 25% | `0.400` | Reactive metabolites & CYP profile |
| PhysChem & LipE | 10% | `0.886` | cLogP, LipE & Ligand Efficiency |
| Developability | 10% | `0.500` | Solubility & microsomal stability |

## 2. Key Calculated Properties
- **Lipophilic Ligand Efficiency (LipE):** `5.12`
- **Ligand Efficiency (LE):** `0.388` kcal/mol/HA
- **Binding Efficiency Index (BEI):** `20.55`
- **Selectivity Window:** `JAK1: 35.0x (>= 30.0x) | JAK3: 56.7x (>= 50.0x) | TYK2: 11.7x (>= 10.0x)`
- **DILI Risk Assessment:** `HIGH`

## 3. Critical Gate Liabilities
- ⚠️ Safety Gate: Severe structural hepatotoxicity or reactive metabolite flag

## 4. Multi-Agent Reasoning Dossier
### Physicochemical & Efficiency Specialist
```
[PhysChem_Efficiency_Specialist] Evaluation for candidate JAK2-TOX-ALERT-003:
- Lipophilic Ligand Efficiency (LipE): 5.12 (Target >= 4.5, Ideal >= 5.5)
- Ligand Efficiency (LE): 0.388 kcal/mol/HA (Target >= 0.32)
- cLogP: 2.8 (Ideal <= 3.0)
- Molecular Weight: 385.4 g/mol, TPSA: 88.5 Å²
  ✅ GATE PASSED: Excellent binding efficiency per heavy atom and well-balanced lipophilicity.
```

### Kinase Potency & Selectivity Specialist
```
[Kinase_Potency_Selectivity_Specialist] Evaluation for candidate JAK2-TOX-ALERT-003:
- JAK2 Enzymatic IC50: 12.0 nM (Target <= 50.0 nM)
- Cellular pSTAT5 IC50: 78.0 nM (Target <= 250.0 nM)
- Isoform Selectivity Folds: JAK1: 35.0x (>= 30.0x) | JAK3: 56.7x (>= 50.0x) | TYK2: 11.7x (>= 10.0x)
  ✅ SELECTIVITY GATE PASSED: Clean selectivity window sparing JAK1, JAK3, and TYK2.
```

### Toxicology & Safety Specialist
```
[ADMET_DILI_Safety_Specialist] Safety evaluation for candidate JAK2-TOX-ALERT-003:
- DILI Risk Tier: HIGH
- Metabolic Stability: HLM T1/2 42.0 min (Target >= 30.0 min)
- CYP Inhibition Status: Clean
- hERG Status: Clean (IC50 18.0 µM)
  ⚠️ IDENTIFIED SAFETY LIABILITIES:
    * Reactive Metabolite Alert: Glutathione (GSH) adduct risk detected
    * Structural DILI Alert: Core scaffold flags HepG2 cytotoxicity risk
```

### Portfolio Governance Lead
```
[MPO_Governance_Decision_Specialist] Synthesis for candidate JAK2-TOX-ALERT-003:
- Composite MPO Score: 0.780 / 1.000 (Advance Threshold: >= 0.75)
  * Potency Pillar (35%): 0.975
  * Selectivity Pillar (20%): 1.000
  * Safety & DILI Pillar (25%): 0.400
  * PhysChem & LipE Pillar (10%): 0.886
  * Developability Pillar (10%): 0.500
- Final Decision Gate Verdict: REJECT_CRITICAL_LIABILITY
  ⚠️ GATE OBSTACLES IDENTIFIED:
    * Safety Gate: Severe structural hepatotoxicity or reactive metabolite flag
```


---

