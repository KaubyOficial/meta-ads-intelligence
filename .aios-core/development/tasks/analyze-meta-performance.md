---
task: analyzeMetaPerformance()
responsável: Alex (@analyst)
responsavel_type: Agente
atomic_layer: Organism
elicit: true
version: "1.0"
story: meta-ads-intelligence
tags:
  - analysis
  - performance
  - insights
---

## Task Definition (AIOS Task Format V1.0)

```yaml
task: analyzeMetaPerformance()

Entrada:
  - campo: focus
    tipo: integer (1-5)
    origem: User Input (elicited)
    obrigatório: true
    validação: Integer between 1 and 5

  - campo: analyst_rules
    tipo: file
    origem: config/analyst-rules.md
    obrigatório: true
    validação: File must exist; rules override all defaults

  - campo: metrics_summary_csv
    tipo: file
    origem: data/processed/metrics_summary.csv
    obrigatório: true

  - campo: campaign_performance_csv
    tipo: file
    origem: data/processed/campaign_performance.csv
    obrigatório: true

  - campo: ad_performance_csv
    tipo: file
    origem: data/processed/ad_performance.csv
    obrigatório: true

Saída:
  - campo: analysis_artifact
    tipo: file (JSON)
    destino: .ai/meta-analysis-{YYYY-MM-DD}.json
    persistido: true
```

---

## Elicitation (Required Before Analysis)

**Before reading any data, ask the user:**

```
═══════════════════════════════════════════════════════════
  Meta Ads Intelligence — Análise de Performance
═══════════════════════════════════════════════════════════

  Qual é o foco principal da análise de hoje?

  1. Saúde geral da conta (spend, resultados, ROAS)
  2. Breakdown por campanha (top/bottom performers)
  3. Análise de criativos (CTR, CPC, frequência por ad)
  4. Detecção de anomalias (quedas, picos, zero delivery)
  5. Análise completa (todos os itens acima)

  Selecione [1-5]:
═══════════════════════════════════════════════════════════
```

Wait for user response before proceeding.

---

## Execution Steps

### Step 0 — MANDATORY: Read analyst-rules.md FIRST

**This step is non-negotiable. Always execute before reading any CSV.**

```
Read: config/analyst-rules.md
```

Extract and apply:
- Override ROAS threshold if specified
- Override CTR low threshold if specified
- Override frequency alert threshold if specified
- Override spend spike multiplier if specified
- Note priority campaigns (always highlight)
- Note campaigns to ignore
- Note what NOT to flag
- Note report language preference

Log which rules were extracted:
```
✓ Rules loaded from config/analyst-rules.md:
  - ROAS threshold: {value} (user) | 2.0 (default)
  - CTR low: {value} | 0.5%
  - Frequency alert: {value} | 3.0
  - Priority campaigns: {list or "none specified"}
  - Ignore list: {list or "none specified"}
```

### Step 1 — Read metrics_summary.csv

Load account-level totals. Key fields to analyze:
- `total_spend`, `total_impressions`, `total_clicks`, `total_results`
- `roas`, `avg_ctr`, `avg_cpm`, `avg_cpc`
- `delta_spend_pct`, `delta_results_pct`, `delta_roas_pct` (if available)

### Step 2 — Read campaign_performance.csv

Load per-campaign data. Sort by spend descending.

### Step 3 — Read ad_performance.csv

Load per-ad data. Sort by spend descending.

### Step 4 — Apply Analysis Framework

Execute based on selected focus:

#### Focus 1: Account Health
- Total spend vs budget (if defined in analyst-rules.md)
- Overall ROAS vs threshold (from rules or default 2.0)
- Overall CTR vs threshold
- Results count and trend (delta%)
- Summary verdict: HEALTHY / ATTENTION / CRITICAL

#### Focus 2: Campaign Breakdown
- Top 3 campaigns by ROAS
- Bottom 3 campaigns by ROAS (with spend > R$50)
- Top 3 campaigns by results
- Campaigns with zero delivery
- Campaigns exceeding frequency threshold
- Priority campaigns performance (from analyst-rules.md)

#### Focus 3: Creative Analysis
- Top 5 ads by CTR
- Bottom 5 ads by CTR (with spend > R$20)
- Top 5 ads by ROAS
- Ads with frequency > threshold → fatigue alert
- Ads with CTR < threshold → poor creative flag

#### Focus 4: Anomaly Detection
- Spend spike: any entity with spend > Nx daily average
- Zero delivery: campaigns/adsets with impressions = 0
- CTR drop: CTR vs previous period delta < -30%
- ROAS collapse: ROAS vs previous period delta < -50%
- Budget pacing issues: spend < 80% of daily budget (if detectable)

#### Focus 5: Complete Analysis
Run all 4 focuses above and compile comprehensive findings.

---

## Built-in Defaults (overridden by analyst-rules.md)

| Metric | Default Threshold | Alert Type |
|--------|------------------|------------|
| ROAS minimum | 2.0 | Below = low performance flag |
| CTR low | 0.5% | Below = creative issue flag |
| Frequency alert | 3.0 | Above = audience fatigue flag |
| Spend spike | 2x daily avg | Above = anomaly flag |
| Zero delivery | 0 impressions | = delivery issue flag |

---

## Output JSON Artifact

Save to: `.ai/meta-analysis-{YYYY-MM-DD}.json`

```json
{
  "date": "YYYY-MM-DD",
  "account_id": "act_XXXX",
  "analysis_focus": 1,
  "analysis_focus_label": "Saúde geral da conta",
  "rules_applied": [
    "ROAS threshold: 3.0 (from analyst-rules.md)",
    "Ignore paused campaigns (from analyst-rules.md)",
    "Priority: Remarketing campaign (from analyst-rules.md)"
  ],
  "summary": {
    "total_spend": 0.00,
    "total_impressions": 0,
    "total_clicks": 0,
    "total_results": 0,
    "roas": 0.00,
    "avg_ctr": 0.00,
    "avg_cpm": 0.00,
    "avg_cpc": 0.00,
    "delta_spend_pct": null,
    "delta_results_pct": null,
    "verdict": "HEALTHY | ATTENTION | CRITICAL"
  },
  "top_campaigns": [
    {
      "campaign_id": "",
      "campaign_name": "",
      "spend": 0.00,
      "roas": 0.00,
      "results": 0,
      "ctr": 0.00,
      "reason": "Highest ROAS"
    }
  ],
  "bottom_campaigns": [],
  "top_ads": [],
  "bottom_ads": [],
  "anomalies": [
    {
      "type": "zero_delivery | spend_spike | ctr_drop | frequency_alert | roas_collapse",
      "entity_type": "campaign | adset | ad",
      "entity_id": "",
      "entity_name": "",
      "metric": "",
      "value": 0,
      "threshold": 0,
      "severity": "HIGH | MEDIUM | LOW",
      "description": ""
    }
  ],
  "insights": [
    "Narrative observation 1",
    "Narrative observation 2"
  ],
  "recommendations": [
    {
      "priority": 1,
      "action": "What to do",
      "entity": "Campaign/Ad name",
      "reason": "Why",
      "impact": "Expected outcome"
    }
  ],
  "data_quality_notes": []
}
```

**All fields must be populated.** Empty arrays are acceptable when there are no findings. Never leave null in numeric fields — use 0 or 0.00.

---

## Post-Conditions

```yaml
post-conditions:
  - [ ] .ai/meta-analysis-{date}.json exists and is valid JSON
    tipo: post-condition
    blocker: true
    error_message: "Artifact not created — analysis may have failed"

  - [ ] rules_applied field is populated (not empty array)
    tipo: post-condition
    blocker: true
    error_message: "analyst-rules.md was not read — re-run task from Step 0"

  - [ ] recommendations array is sorted by priority (1=highest)
    tipo: post-condition
    blocker: false
    error_message: "Recommendations should be prioritized"
```

---

## Performance

```yaml
duration_expected: 10-20 min (depending on account size and focus)
cost_estimated: $0.01-0.05 (Claude API tokens for analysis)
token_usage: ~10,000-50,000 tokens
```
