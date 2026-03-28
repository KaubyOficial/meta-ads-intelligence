# Meta Ads Intelligence Report — {{DATE}}

**Conta:** {{ACCOUNT_ID}}
**Período:** {{DATE_SINCE}} a {{DATE_UNTIL}}
**Análise gerada por:** @analyst
**Foco:** {{ANALYSIS_FOCUS_LABEL}}

---

## Resumo Executivo

| KPI | Hoje | Variação (7d) |
|-----|------|---------------|
| Spend Total | {{TOTAL_SPEND}} | {{DELTA_SPEND}} |
| Resultados | {{TOTAL_RESULTS}} | {{DELTA_RESULTS}} |
| ROAS | {{ROAS}} | {{DELTA_ROAS}} |
| CTR Médio | {{AVG_CTR}}% | — |
| CPM Médio | {{AVG_CPM}} | — |
| CPC Médio | {{AVG_CPC}} | — |
| Impressões | {{TOTAL_IMPRESSIONS}} | — |
| Cliques | {{TOTAL_CLICKS}} | — |

**Veredicto da conta:** {{VERDICT}}

---

## Principais Insights

{{NARRATIVE_INSIGHTS}}

---

## Top Campanhas

| Campanha | Tipo | Spend | ROAS | Resultados | CTR | Status |
|----------|------|-------|------|------------|-----|--------|
{{TOP_CAMPAIGNS_TABLE}}

> **Legenda de tipo:** `[ASC]` Advantage+ Sales · `[ADV+ AUD]` Advantage+ Audience · `[MANUAL]` Campanha manual F1/F2/F3

---

## Campanhas Críticas — Atenção Necessária

| Campanha | Tipo | Spend | ROAS | CTR | Problema | Ação Recomendada |
|----------|------|-------|------|-----|----------|------------------|
{{BOTTOM_CAMPAIGNS_TABLE}}

---

## Análise de Audiência

| Campanha | Tipo Audiência | Frequência | CPM | CTR | Sinal Saturação |
|----------|---------------|------------|-----|-----|-----------------|
{{AUDIENCE_ANALYSIS_TABLE}}

> **Thresholds:** Freq > 3.0x (F2) / > 2.5x (F3) = alerta fadiga · CPM > R$35 = audiência saturando · CTR < 0.5% = revisar hook
> **Ref:** `docs/meta-knowledge/audience-intelligence-guide.md`

---

## Anomalias Detectadas

{{ANOMALIES_SECTION}}

---

## Análise de Criativos

| Anúncio | Campanha | CTR | CPC | Frequência | ROAS | Verdict |
|---------|----------|-----|-----|------------|------|---------|
{{ADS_TABLE}}

---

## Recomendações

> Ordenadas por impacto estimado (1 = mais urgente)

{{RECOMMENDATIONS_LIST}}

---

## Contexto de Atribuição

- **Janela:** 7-day click (padrão da conta)
- **Fonte de faturamento:** `vendas_*.csv` (Hotmart) — fonte de verdade
- **Fonte de CPA por criativo:** `ads_*.csv` — Pixel Meta (subestima ~20-40% das conversões reais)
- **Nota iOS 14+:** Divergência entre Pixel e faturamento real é esperada e normal.
- **7-day view:** Depreciada em Jan/2026 — não disponível.

---

## Regras Aplicadas

> Regras definidas em `config/analyst-rules.md` que foram utilizadas nesta análise:

{{RULES_APPLIED_LIST}}

---

## Referência de Dados

| Arquivo | Conteúdo |
|---------|----------|
| `data/processed/metrics_summary.csv` | Totais da conta por dia |
| `data/processed/campaign_performance.csv` | KPIs por campanha |
| `data/processed/ad_performance.csv` | KPIs por anúncio |
| `.ai/meta-analysis-{{DATE}}.json` | Artifact de análise completo |

---

*Gerado pelo Meta Ads Intelligence System — Synkra AIOS*
*Fase: Read-Only — Todas as recomendações requerem revisão humana antes de execução*
