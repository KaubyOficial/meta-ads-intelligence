# Meta Ads Intelligence — Resumo Semanal

**Conta:** {{ACCOUNT_ID}}
**Semana:** {{WEEK_START}} a {{WEEK_END}} (Semana {{WEEK_NUMBER}})
**Comparativo:** vs semana anterior ({{PREV_WEEK_START}} a {{PREV_WEEK_END}})
**Análise gerada por:** @analyst

---

## Resumo da Semana

| KPI | Semana Atual | Semana Anterior | Variação |
|-----|-------------|-----------------|----------|
| Spend Total | {{WEEK_SPEND}} | {{PREV_WEEK_SPEND}} | {{DELTA_SPEND}}% |
| Resultados | {{WEEK_RESULTS}} | {{PREV_WEEK_RESULTS}} | {{DELTA_RESULTS}}% |
| ROAS Médio | {{WEEK_ROAS}} | {{PREV_WEEK_ROAS}} | {{DELTA_ROAS}}% |
| CTR Médio | {{WEEK_CTR}}% | {{PREV_WEEK_CTR}}% | {{DELTA_CTR}}% |
| CPC Médio | {{WEEK_CPC}} | {{PREV_WEEK_CPC}} | {{DELTA_CPC}}% |
| Impressões | {{WEEK_IMPRESSIONS}} | {{PREV_WEEK_IMPRESSIONS}} | {{DELTA_IMPRESSIONS}}% |

**Tendência geral:** {{WEEK_VERDICT}}

---

## Evolução Diária (Spend & Resultados)

| Data | Spend | Resultados | ROAS | CTR |
|------|-------|------------|------|-----|
{{DAILY_BREAKDOWN_TABLE}}

---

## Top Campanhas da Semana

| # | Campanha | Tipo | Spend | ROAS | Resultados | vs Semana Anterior |
|---|----------|------|-------|------|------------|-------------------|
{{TOP_CAMPAIGNS_WEEKLY_TABLE}}

> **Legenda de tipo:** `[ASC]` Advantage+ Sales · `[ADV+ AUD]` Advantage+ Audience · `[MANUAL]` F1/F2/F3 manual

---

## Campanhas que Pioraram

| Campanha | ROAS Atual | ROAS Anterior | Variação | Possível Causa |
|----------|------------|---------------|----------|----------------|
{{DECLINING_CAMPAIGNS_TABLE}}

---

## Análise de Criativos da Semana

### Melhores Criativos

| Anúncio | CTR | CPC | ROAS | Frequência | Status |
|---------|-----|-----|------|------------|--------|
{{TOP_ADS_WEEKLY_TABLE}}

### Criativos com Sinais de Fadiga

| Anúncio | Frequência | CTR | Tendência | Recomendação |
|---------|------------|-----|-----------|--------------|
{{FATIGUED_ADS_TABLE}}

---

## Análise de Audiência da Semana

| Campanha | Tipo | Freq. Média | CPM Médio | CTR Médio | Status Saturação |
|----------|------|-------------|-----------|-----------|-----------------|
{{AUDIENCE_WEEKLY_TABLE}}

> **Alertas:** Freq > 3.0x (F2) / > 2.5x (F3) · CPM subindo > 20%/semana · CTR caindo > 30%/semana
> **Ref:** `docs/meta-knowledge/audience-intelligence-guide.md`

---

## Anomalias da Semana

{{WEEKLY_ANOMALIES_SECTION}}

---

## Insights Estratégicos

{{WEEKLY_STRATEGIC_INSIGHTS}}

---

## Recomendações para a Próxima Semana

> Ordenadas por impacto estimado

{{WEEKLY_RECOMMENDATIONS}}

---

## Orçamento — Distribuição por Fase

| Fase | Gasto | % do Total | N° Camps | Referência Ideal |
|------|-------|-----------|---------|-----------------|
{{BUDGET_FASE_TABLE}}

> **Referência:** F1 10–15% · F2 30–40% · F3 40–50% · RMKT 5–10%

---

## Orçamento — Análise de Pacing

| Campanha | Budget Semanal | Spend Real | Pacing | Status |
|----------|---------------|------------|--------|--------|
{{BUDGET_PACING_TABLE}}

---

## Contexto de Atribuição

- **Janela:** 7-day click (padrão da conta)
- **Fonte de faturamento:** `vendas_*.csv` (Hotmart) — fonte de verdade
- **Fonte de CPA por criativo:** `ads_*.csv` — Pixel Meta (subestima ~20-40% das conversões reais)
- **Nota iOS 14+:** Divergência entre Pixel e faturamento real é esperada e normal.
- **7-day view:** Depreciada em Jan/2026 — não disponível.

---

## Regras Aplicadas

> Regras de `config/analyst-rules.md` utilizadas nesta análise:

{{RULES_APPLIED_LIST}}

---

## Referência de Dados

| Arquivo | Conteúdo |
|---------|----------|
| `data/processed/metrics_summary.csv` | Totais diários da conta |
| `data/processed/campaign_performance.csv` | KPIs por campanha |
| `data/processed/ad_performance.csv` | KPIs por anúncio |
| `.ai/meta-analysis-*.json` | Artifacts de análise (7 dias) |

---

*Gerado pelo Meta Ads Intelligence System — Synkra AIOS*
*Fase: Read-Only — Todas as recomendações requerem revisão humana antes de execução*
