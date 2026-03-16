---
task: fetchMetaData()
responsável: Dev (@dev)
responsavel_type: Agente
atomic_layer: Organism
elicit: false
version: "1.0"
story: meta-ads-intelligence
tags:
  - data-collection
  - meta-api
  - automation
---

## Task Definition (AIOS Task Format V1.0)

```yaml
task: fetchMetaData()

Entrada:
  - campo: date_range
    tipo: string
    origem: User Input or Default
    obrigatório: false
    validação: >
      Preset: today, yesterday, last_7d, last_14d, last_30d, last_60d,
      last_90d, last_180d, last_365d, this_month, last_month,
      this_quarter, last_quarter, this_semester, last_semester,
      this_year, last_year.
      Or use --since/--until for custom ranges.
    default: yesterday

  - campo: since
    tipo: string (YYYY-MM-DD)
    origem: User Input
    obrigatório: false
    validação: ISO date format. Overrides date_range.

  - campo: until
    tipo: string (YYYY-MM-DD)
    origem: User Input
    obrigatório: false
    validação: ISO date format. Defaults to yesterday if --since is given.

  - campo: account_id
    tipo: string
    origem: .env (META_AD_ACCOUNT_ID)
    obrigatório: true
    validação: Must start with "act_" or be set in .env

Saída:
  - campo: raw_json_files
    tipo: files
    destino: data/raw/{campaigns,adsets,ads,insights}/
    persistido: true

  - campo: manifest
    tipo: file
    destino: data/raw/{date}_manifest.json
    persistido: true

  - campo: processed_csvs
    tipo: files
    destino: data/processed/
    persistido: true
```

---

## Pre-Conditions

```yaml
pre-conditions:
  - [ ] .env file exists with META_ACCESS_TOKEN and META_AD_ACCOUNT_ID
    tipo: pre-condition
    blocker: true
    validação: Check that .env exists and has non-empty token values
    error_message: "Missing .env — copy .env.example to .env and fill in credentials"

  - [ ] Python 3.8+ is available
    tipo: pre-condition
    blocker: true
    validação: python --version or python3 --version
    error_message: "Python not found. Install Python 3.8+"

  - [ ] facebook-business SDK installed
    tipo: pre-condition
    blocker: true
    validação: python -c "import facebook_business"
    error_message: "SDK missing. Run: pip install -r scripts/requirements.txt"

  - [ ] pandas installed
    tipo: pre-condition
    blocker: true
    validação: python -c "import pandas"
    error_message: "pandas missing. Run: pip install -r scripts/requirements.txt"
```

---

## Execution Steps

### Step 1 — Run Collector

```bash
# Preset
python scripts/meta_collector.py --date-range {date_range}

# Custom range
python scripts/meta_collector.py --since 2025-01-01 --until 2025-06-30

# Or import external file instead of API fetch
python scripts/data_importer.py --file export.csv --date-label 2025-01-15 --also-process
```

**Expected output:**
- `data/raw/campaigns/{date}_campaigns.json`
- `data/raw/adsets/{date}_adsets.json`
- `data/raw/ads/{date}_ads.json`
- `data/raw/insights/{date}_insights.json`
- `data/raw/{date}_manifest.json`

**Status messages to show:**
```
[1/5] Fetching campaigns...
[2/5] Fetching ad sets...
[3/5] Fetching ads...
[4/5] Fetching insights...
[5/5] Writing manifest...
```

### Step 2 — Validate Raw Files

Check that all 4 entity JSON files exist and are non-empty:

```python
import json
from pathlib import Path

date_label = # resolved from date_range
raw_dir = Path("data/raw")

files_to_check = [
    raw_dir / "campaigns" / f"{date_label}_campaigns.json",
    raw_dir / "adsets" / f"{date_label}_adsets.json",
    raw_dir / "ads" / f"{date_label}_ads.json",
    raw_dir / "insights" / f"{date_label}_insights.json",
]

for f in files_to_check:
    if not f.exists():
        print(f"WARNING: Missing {f}")
    else:
        data = json.loads(f.read_text())
        if len(data) == 0:
            print(f"WARNING: {f.name} is empty — no data for this period")
        else:
            print(f"OK: {f.name} ({len(data)} records)")
```

### Step 3 — Run Processor

```bash
python scripts/data_processor.py --date {date_since}
```

**Expected output:**
- `data/processed/metrics_summary.csv`
- `data/processed/campaign_performance.csv`
- `data/processed/ad_performance.csv`

### Step 4 — Validate CSVs

```python
import pandas as pd
from pathlib import Path

processed_dir = Path("data/processed")
csvs = ["metrics_summary.csv", "campaign_performance.csv", "ad_performance.csv"]

for csv_name in csvs:
    path = processed_dir / csv_name
    if not path.exists():
        print(f"ERROR: {csv_name} not created")
        continue
    df = pd.read_csv(path)
    critical = {"spend", "impressions", "clicks"} & set(df.columns)
    nans = {col: df[col].isna().sum() for col in critical}
    bad = {k: v for k, v in nans.items() if v > 0}
    if bad:
        print(f"WARNING {csv_name}: NaN in {bad}")
    else:
        print(f"OK: {csv_name} ({len(df)} rows)")
```

### Step 5 — Print Summary

```
╔══════════════════════════════════════════════════╗
║     Meta Ads Data Collection — Complete          ║
╠══════════════════════════════════════════════════╣
║  Campaigns:     {N}                              ║
║  Ad Sets:       {N}                              ║
║  Ads:           {N}                              ║
║  Insight rows:  {N}                              ║
╠══════════════════════════════════════════════════╣
║  Processed CSVs:                                 ║
║  ✓ metrics_summary.csv     ({N} rows)            ║
║  ✓ campaign_performance.csv ({N} rows)           ║
║  ✓ ad_performance.csv      ({N} rows)            ║
╚══════════════════════════════════════════════════╝

Ready for analysis: *task analyze-meta-performance
```

---

## Post-Conditions

```yaml
post-conditions:
  - [ ] 4 JSON files exist in data/raw/
    tipo: post-condition
    blocker: true
    validação: All 4 entity files exist (empty is acceptable if account has no data)
    error_message: "Raw JSON files not created — check collector error output"

  - [ ] manifest.json exists with counts
    tipo: post-condition
    blocker: true
    validação: Manifest file readable and has "counts" key
    error_message: "Manifest not written — collector may have failed"

  - [ ] 3 CSVs exist in data/processed/
    tipo: post-condition
    blocker: true
    validação: All 3 CSV files exist
    error_message: "CSVs not created — check processor error output"
```

---

## Error Handling

| Error | Code | Action |
|-------|------|--------|
| Rate limit | 80000 | Backoff 2^n seconds, max 5 retries |
| Invalid token | 190, 102 | HALT with message: "Update META_ACCESS_TOKEN in .env" |
| No .env | — | HALT with message: "Copy .env.example to .env" |
| SDK missing | ImportError | HALT with message: "Run pip install -r scripts/requirements.txt" |
| No data returned | — | Continue with WARNING, empty JSONs are valid |

---

## Performance

```yaml
duration_expected: 3-10 min (depends on account size and rate limits)
cost_estimated: API calls only (Meta Marketing API — free for read)
token_usage: ~2,000-5,000 tokens
```
