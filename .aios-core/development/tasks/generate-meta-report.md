---
task: generateMetaReport()
responsável: Alex (@analyst)
responsavel_type: Agente
atomic_layer: Organism
elicit: false
version: "1.0"
story: meta-ads-intelligence
tags:
  - report
  - markdown
  - documentation
---

## Task Definition (AIOS Task Format V1.0)

```yaml
task: generateMetaReport()

Entrada:
  - campo: analysis_artifact
    tipo: file (JSON)
    origem: .ai/meta-analysis-{YYYY-MM-DD}.json
    obrigatório: true
    validação: File must exist and be valid JSON

  - campo: template
    tipo: string
    origem: User Input or Default
    obrigatório: false
    validação: "daily" | "weekly"
    default: daily

  - campo: daily_template
    tipo: file
    origem: templates/daily-report-tmpl.md
    obrigatório: true

Saída:
  - campo: report
    tipo: file (Markdown)
    destino: docs/reports/{YYYY-MM-DD}-daily-report.md
    persistido: true
```

---

## Pre-Conditions

```yaml
pre-conditions:
  - [ ] .ai/meta-analysis-{date}.json exists
    tipo: pre-condition
    blocker: true
    error_message: "Run analyze-meta-performance task first"

  - [ ] templates/daily-report-tmpl.md exists
    tipo: pre-condition
    blocker: true
    error_message: "Template file missing — check templates/ directory"
```

---

## Execution Steps

### Step 1 — Load Analysis Artifact

```
Read: .ai/meta-analysis-{date}.json
```

Verify all required sections are present:
- `summary`, `top_campaigns`, `bottom_campaigns`, `anomalies`
- `insights`, `recommendations`, `rules_applied`

### Step 2 — Load Template

Select template based on input:
- If `template == "daily"` (default): load `templates/daily-report-tmpl.md`
- If `template == "weekly"`: load `templates/weekly-summary-tmpl.md`

```
Read: templates/{template_file}
```

### Step 2.5 — Placeholder Mapping Reference

Use this mapping to connect JSON artifact fields to template placeholders:

```yaml
placeholder_mapping:
  "{{DATE}}": "date"
  "{{ACCOUNT_ID}}": "account_id"
  "{{DATE_SINCE}}": "derived from date range"
  "{{DATE_UNTIL}}": "derived from date range"
  "{{ANALYSIS_FOCUS_LABEL}}": "analysis_focus_label"
  "{{TOTAL_SPEND}}": "summary.total_spend"
  "{{TOTAL_RESULTS}}": "summary.total_results"
  "{{ROAS}}": "summary.roas"
  "{{AVG_CTR}}": "summary.avg_ctr"
  "{{AVG_CPM}}": "summary.avg_cpm"
  "{{AVG_CPC}}": "summary.avg_cpc"
  "{{TOTAL_IMPRESSIONS}}": "summary.total_impressions"
  "{{TOTAL_CLICKS}}": "summary.total_clicks"
  "{{DELTA_SPEND}}": "summary.delta_spend_pct"
  "{{DELTA_RESULTS}}": "summary.delta_results_pct"
  "{{DELTA_ROAS}}": "computed from summary"
  "{{VERDICT}}": "summary.verdict"
  "{{NARRATIVE_INSIGHTS}}": "insights[] → render as paragraphs"
  "{{TOP_CAMPAIGNS_TABLE}}": "top_campaigns[] → render as MD table"
  "{{BOTTOM_CAMPAIGNS_TABLE}}": "bottom_campaigns[] → render as MD table"
  "{{ANOMALIES_SECTION}}": "anomalies[] → render grouped by severity"
  "{{ADS_TABLE}}": "top_ads[] + bottom_ads[] → render as MD table"
  "{{RECOMMENDATIONS_LIST}}": "recommendations[] → render as numbered list"
  "{{RULES_APPLIED_LIST}}": "rules_applied[] → render as bullet list"
```

### Step 3 — Populate Report

Replace every `{{PLACEHOLDER}}` in the template with real data from the JSON artifact, using the mapping above.

**For each section:**

#### Executive Summary Table
Use `summary` object. Format spend as currency. Show delta arrows:
- Positive delta: ↑ {value}%
- Negative delta: ↓ {value}%
- No delta data: —

#### Insights Section
Expand each string in `insights` array into narrative paragraphs. Add context and interpretation. Do NOT just copy the strings verbatim — write as a skilled analyst would.

#### Top Campaigns Table
Render `top_campaigns` array as Markdown table with columns:
| Campanha | Spend | ROAS | Resultados | CTR | Status |

#### Critical Campaigns Table
Render `bottom_campaigns` with emphasis on WHY they're underperforming.
Include recommended action for each.

#### Anomalies Section
For each anomaly in `anomalies` array:
- Group by severity (HIGH first)
- Include entity name, metric, value vs threshold
- Suggest immediate action

#### Creative Analysis Table
From `top_ads` and `bottom_ads`:
| Anúncio | Campanha | CTR | CPC | Frequência | ROAS | Verdict |

#### Recommendations
Render numbered list from `recommendations` sorted by priority.
For each: **Action** — Reason — Expected impact.

#### Rules Applied Section
List each rule from `rules_applied` array as bullet points.
This section is MANDATORY — never omit.

#### Data Reference
List paths to source files used:
- `data/processed/metrics_summary.csv`
- `data/processed/campaign_performance.csv`
- `data/processed/ad_performance.csv`
- `.ai/meta-analysis-{date}.json`

### Step 4 — Validate No Placeholders Remain

Scan the generated report for `{{` patterns. If any remain:
- Log which placeholders are missing
- Fill with "N/A" or appropriate empty value
- Never deliver a report with unfilled placeholders

### Step 5 — Save Report

```
Write: docs/reports/{date}-daily-report.md
```

Print confirmation:
```
✓ Report generated: docs/reports/{date}-daily-report.md
  Sections: Executive Summary | Insights | Top/Bottom Campaigns | Anomalies | Creatives | Recommendations | Rules
  Recommendations: {N} actions (sorted by priority)
  Anomalies found: {N}
```

---

## Post-Conditions

```yaml
post-conditions:
  - [ ] docs/reports/{date}-daily-report.md exists
    tipo: post-condition
    blocker: true
    error_message: "Report file not created"

  - [ ] No {{PLACEHOLDER}} patterns in the generated file
    tipo: post-condition
    blocker: true
    error_message: "Report has unfilled placeholders — review template population"

  - [ ] Section "Regras Aplicadas" is present and non-empty
    tipo: post-condition
    blocker: true
    error_message: "Rules Applied section must always be present"

  - [ ] Recommendations are numbered and sorted (1=highest priority first)
    tipo: post-condition
    blocker: false
    error_message: "Sort recommendations by business impact"
```

---

## Performance

```yaml
duration_expected: 5-10 min
cost_estimated: $0.005-0.02 (template rendering)
token_usage: ~5,000-15,000 tokens
```
