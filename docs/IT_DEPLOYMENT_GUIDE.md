# IT & Software Engineering Guide: JAK2 Kinase Optimizer

This guide covers architecture, automated testing, containerization, and enterprise integrations for IT, DevOps, and Data Engineering teams.

---

## 1. System Requirements & Environment Setup

* **Python Runtime:** Python 3.10 to 3.13 (verified on Python 3.13.3 Windows AMD64).
* **Package Management:** Standard `venv` + `pip` (or `uv` / `poetry`).
* **Framework:** Google Agent Development Kit (`google-adk>=2.12.0`).

### Clean Setup from Source:
```bash
git clone <repo-url>
cd Research_Rover

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install locked dependencies
pip install -r requirements.txt
pip install -e .
```

---

## 2. Google ADK Multi-Agent Orchestration

The pipeline is structured using Google ADK's `SequentialAgent` abstraction:

```python
from google.adk.agents import SequentialAgent
from jak2_adk.workflow import JAK2ScreeningOrchestrator

orchestrator = JAK2ScreeningOrchestrator()
adk_agent = orchestrator.build_adk_sequential_agent()

print(f"Agent Name: {adk_agent.name}")
print(f"Registered Sub-agents: {[s.name for s in adk_agent.sub_agents]}")
```

### Agent Roles:
1. `PhysChem_Efficiency_Specialist`: Wraps `calculate_efficiency_metrics`.
2. `Kinase_Potency_Selectivity_Specialist`: Wraps `evaluate_selectivity_ratios`.
3. `ADMET_DILI_Safety_Specialist`: Wraps `screen_toxicology_alerts`.
4. `MPO_Governance_Decision_Specialist`: Wraps `compute_mpo_score`.

---

## 3. Database / Data Warehouse Batch Ingestion

You can connect the screening pipeline directly to your data warehouse (BigQuery, PostgreSQL, Snowflake) or Electronic Lab Notebook (ELN) using Pandas or Polars:

```python
import pandas as pd
from jak2_adk.models import CandidateInput
from jak2_adk.workflow import JAK2ScreeningOrchestrator

# 1. Query candidates from SQL or CSV
query_sql = "SELECT candidate_id, mw, clogp, tpsa, hbd, hba, rot_bonds, heavy_atom_count, jak2_ic50_nm, jak1_ic50_nm, jak3_ic50_nm, tyk2_ic50_nm, cellular_pstat5_ic50_nm, hlm_half_life_min, solubility_ug_ml, cyp3a4_ic50_um, cyp2d6_ic50_um, cyp2c9_ic50_um, herg_ic50_um, reactive_metabolite_risk, hepatotoxicity_alert, pains_alert FROM assay_screening_table WHERE campaign = 'JAK2_2026';"
# df = pd.read_sql(query_sql, connection)

df = pd.read_csv("batch_assay_data.csv")
candidates = [CandidateInput(**row) for row in df.to_dict(orient="records")]

# 2. Run Orchestrated Triage
orchestrator = JAK2ScreeningOrchestrator()
reports = orchestrator.evaluate_batch(candidates)

# 3. Export Decisions
out_rows = []
for r in reports:
    out_rows.append({
        "candidate_id": r.candidate_id,
        "verdict": r.verdict.value,
        "mpo_score": r.composite_mpo,
        "lipe": r.efficiency.lipe,
        "dili_risk": r.toxicology.dili_risk_level,
        "gate_failures": " | ".join(r.gate_failures)
    })

pd.DataFrame(out_rows).to_csv("triage_decisions.csv", index=False)
```

---

## 4. Docker Containerization

To run the optimizer as an isolated microservice:

### `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

COPY jak2_adk/ ./jak2_adk/
COPY examples/ ./examples/
COPY generate_visualizations.py package_share.py ./

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python", "-m", "jak2_adk.cli"]
CMD ["--demo"]
```

### Build & Run:
```bash
docker build -t jak2-optimizer .
docker run --rm jak2-optimizer --demo
```

---

## 5. Google Cloud Run Deployment via Google ADK CLI

If using Google ADK's native deployment features to host on **Google Cloud Run**:

```bash
# Set your Google Cloud project
gcloud config set project <PROJECT_ID>

# Deploy using Google ADK
adk deploy cloud_run --service-name jak2-screening-service --region us-central1
```

---

## 6. Automated Testing & CI/CD Pipeline

The project includes 12 automated unit and integration tests located in `tests/`:

```powershell
# Run tests
pytest -v

# Run with coverage
pytest --cov=jak2_adk tests/
```

### GitHub Actions Workflow (`.github/workflows/ci.yml`):
```yaml
name: JAK2 Optimizer CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e .
      - name: Run Pytest
        run: pytest -v
```
