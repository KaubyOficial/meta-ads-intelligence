# Meta Ads Intelligence — Claude Code Configuration

## Project Purpose

Read-only Meta Marketing API intelligence system. Collects ad account data, processes it into CSVs, analyzes performance with @analyst, and generates structured reports.

**Phase: Read-Only** — No writes to Meta API. All actions are local. User reviews all recommendations before acting.

---

## Master AIOS

> **Ler `.aios-core/master.md` para configuração completa de agentes, comandos, protocolo anti-interferência e biblioteca central.**

---

## Key Paths

| Path | Description |
|------|-------------|
| `.aios-core/master.md` | **MASTER CONFIG** — agentes, comandos, constantes, protocolo anti-interferência |
| `scripts/aios_utils.py` | **BIBLIOTECA CENTRAL** — todos os parsers testados. Usar em todo script novo. |
| `config/analyst-rules.md` | **Leitura obrigatória antes de toda análise** — rota definitiva (Seção 10) + precisão numérica (Seção 11) |
| `config/account-benchmarks.md` | Benchmarks históricos — fev/26 como referência |
| `data/sheets/` | **FONTE DE VERDADE (TIER 1)** — CSVs do Google Sheets — gasto, vendas, criativos |
| `data/processed/` | **TIER 2** — só para ads_*.csv quando sheets não cobrir |
| `data/raw/` | **TIER 3 — IMUTÁVEL** — Raw JSON Meta API — nunca editar |
| `docs/reports/` | Relatórios Markdown gerados |
| `.ai/` | Artifacts JSON de análise — gitignored |
| `.aios-core/development/tasks/` | Definições de tasks AIOS (fetch, analyze, report) |
| `.aios-core/development/workflows/` | Pipeline guiado `*workflow` |
| `scripts/meta_collector.py` | Coleta Meta API → `data/raw/` (opcional, secundário) |
| `scripts/sheets_collector.py` | **Coleta primária** Google Sheets → `data/sheets/` |
| `scripts/data_processor.py` | Normaliza JSONs → `data/processed/` |

---

## Fonte de Verdade — Google Sheets (data/sheets/)

> **SEMPRE usar `data/sheets/` como fonte primária.** Nunca usar `data/processed/` para faturamento ou vendas.

### Arquivos e seus usos

| Arquivo | Fonte de | Colunas-chave | Filtros obrigatórios |
|---------|----------|---------------|---------------------|
| `{date}_diario_mda.csv` | Gasto MDA, IC, Cliques | `Gasto`, `IC`, `Impressões`, `Cliques no Link` | Filtrar por `Data` no período |
| `{date}_diario_lvc.csv` | Gasto LVC, IC, Cliques | `Gasto`, `IC`, `Impressões`, `Cliques no Link` | Filtrar por `Data` no período |
| `{date}_diario_teus.csv` | Gasto TEUS, IC, Cliques | `Gasto`, `IC`, `Impressões`, `Cliques no Link` | Filtrar por `Data` no período |
| `{date}_vendas_mda.csv` | Faturamento MDA real | `VALOR PAGO`, `PRODUTO`, `STATUS`, `UTM_CONTENT`, `TRANSACTION` | `STATUS IN ('APPROVED','COMPLETE')` |
| `{date}_vendas_lvc.csv` | Faturamento LVC real (esteira) | `VALOR PAGO`, `PRODUTO`, `STATUS`, `UTM_CONTENT`, `TRANSACTION` | `STATUS IN ('APPROVED','COMPLETE')` |
| `{date}_vendas_teus.csv` | Faturamento TEUS real | `VALOR PAGO`, `PRODUTO`, `STATUS`, `UTM_CONTENT`, `TRANSACTION` | `STATUS IN ('APPROVED','COMPLETE')` |
| `{date}_reembolsos.csv` | Reembolsos por criativo | `VALOR REEMBOLSADO`, `PRODUTO`, `UTM_CONTENT` | Filtrar por `DATA` no período |
| `{date}_ads_mda.csv` | Criativos MDA (Meta API + planilha) | `NOME ADS`, `GASTO`, `COMPRAS`, `IMPRESSÕES`, `CLIQUES` | Filtrar por `DATA` no período |
| `{date}_ads_teus.csv` | Criativos TEUS | `NOME ADS`, `GASTO`, `COMPRAS`, `IMPRESSÕES`, `CLIQUES` | Filtrar por `DATA` no período |
| `{date}_vendas_acelerador_comercial.csv` | ~~Acelerador~~ | **IGNORAR** | Excluir de todos os cálculos |
| `{date}_vendas_upsell_acelerador.csv` | ~~Upsell Acelerador~~ | **IGNORAR** | Excluir de todos os cálculos |

### Regras de STATUS (vendas_*.csv)

```
APPROVED  → CONTA no faturamento
COMPLETE  → CONTA no faturamento
REFUNDED  → NÃO CONTA (estorno)
PROTESTED → NÃO CONTA (chargeback)
```

### Produto Principal por arquivo

```
vendas_mda.csv   → PRODUTO contém "Mestres do Algoritmo"
vendas_lvc.csv   → PRODUTO contém "Lucrando com Vídeos Curtos"
vendas_teus.csv  → PRODUTO contém "Lucrando com Vídeos Curtos"
  (TEUS é estrutura de campanha que vende produto LVC)
```

### Campanhas ativas (março/2026)

```
MDA   → rodando  → diario_mda + vendas_mda
TEUS  → rodando  → diario_teus + vendas_teus
LVC   → parado desde ~09/03/2026, mas:
          - receita LVC (esteira/orgânico) CONTA no faturamento → vendas_lvc
          - gasto LVC entra se rodou no período analisado → diario_lvc
```

---

## Default Agent

**@analyst** — Primary agent for analysis and report generation.

For data collection tasks, use **@dev**.

---

## Workflow

```
*workflow meta-ads-intelligence
```

### Etapas — 5 Steps

**1. collect-data** (@dev)
- `sheets_collector.py` → `data/sheets/` (vendas + ads + diário de todas as ofertas)
- `meta_collector.py` → `data/raw/` (Meta API)
- `data_processor.py` → `data/processed/`

**2. validate-data** (@analyst)
- Verifica integridade dos dados coletados (gaps de datas, colunas ausentes, linhas zero)
- Confirma que sheets e processed estão alinhados temporalmente
- Bloqueia análise se dados críticos estiverem ausentes
- Output: `validated: true/false` no artifact

**3. analyze-campaigns** (@analyst)
- Lê: `config/analyst-rules.md`, `config/account-benchmarks.md`
- Lê: `data/processed/campaign_performance.csv`
- Classifica cada campanha por fase: F1 / F2 / F3 / RMKT / F0 (via prefixo ou padrão no nome)
- Separa tráfego frio `[F]` vs quente `[Q]`
- Calcula CPA por campanha e compara com targets (ALVO / BOM / LIMITE / CORTE)
- Identifica janelas de orçamento (7 dias) — NÃO recomendar ajuste dentro da janela
- Verifica ROAS vs benchmarks históricos (`account-benchmarks.md`)
- Output: seção `campaigns` no artifact JSON

**4. analyze-creatives** (@analyst)
- Lê: `data/processed/ad_performance.csv`
- Lê: `data/sheets/{date}_ads_mda.csv`, `ads_lvc.csv`, `ads_teus.csv`
- Lê: `data/sheets/{date}_vendas_mda.csv`, `vendas_lvc.csv`, `vendas_teus.csv` (correlação UTM)
- Lê: `data/sheets/{date}_diario_mda.csv`, `diario_lvc.csv`, `diario_teus.csv`
- Ranking de criativos por CPA dentro de cada fase
- Identifica candidatos a promoção (CPA ≤ R$ 102,35 em F1)
- Identifica candidatos a corte (CPA > R$ 153,53 + sem venda em 2 dias)
- Compara VSL A vs VSL B vs VSL C por produto
- Verifica frequência (fadiga): F2/F3 > 3.0x, F3 > 2.5x = alerta
- Correlaciona UTM_CONTENT das vendas com Ad Name dos criativos
- Output: seção `creatives` no artifact JSON

**5. generate-report** (@analyst)
- Lê artifact JSON de etapas 3 e 4
- Gera `docs/reports/YYYY-MM-DD-weekly-report.md`
- Estrutura obrigatória:
  - Resumo executivo (investimento, vendas, ROAS, vs benchmark)
  - Tabela por campanha (fase, gasto, CPA, status)
  - Ranking de criativos com recomendação (promover / manter / pausar)
  - VSL A vs VSL B vs VSL C por produto
  - Movimentações recomendadas (prioridade 1–5)
  - Checklist da semana
  - Alertas críticos (cortes urgentes)

---

## Critical Rules

### data/raw/ is Immutable
- Never edit raw JSON files manually
- Re-run `meta_collector.py` to refresh
- Raw files are gitignored — do not commit

### analyst-rules.md is Always Read First
- Every analysis MUST read `config/analyst-rules.md` before applying defaults
- User rules override all built-in thresholds
- Field `rules_applied` in the JSON artifact must list which rules were used

### Idempotency
- All scripts can be re-run for the same date without duplicating data
- Existing files are overwritten, not appended

### Read-Only Phase
- No modifications to Meta API (no budget changes, no pause/start, no edits)
- Scripts only perform GET requests
- All recommendations are for user review only

---

## Vocabulário de Comandos (*)

> Sempre usar dados mais recentes em `data/sheets/`.
> Se desatualizados (> 1 dia): avisar e oferecer `*collect` primeiro.
> Sempre cruzar `diario_*` + `ads_*` + `reembolsos`. Nunca inventar números.
> Ticket médio fixo: R$ 196,10. CPA Alvo R$98,05 | Bom R$108,94 | Limite R$130,73 | Corte R$163,42.

---

### PULSO DIÁRIO — checar o estado geral a qualquer momento

```
*status    │ Painel geral — gasto, vendas, CPA, ROAS, checkout por produto
*hoje      │ Performance do dia atual
*ontem     │ Performance de ontem
*semana    │ Semana atual (segunda → hoje)
*pausar    │ Alertas críticos — o que pausar agora, sem enrolação
*collect   │ Forçar coleta fresca das planilhas agora
```

Exemplos de ativação:
```
"como foi essa semana?"           → *status
"me dá um resumo de hoje"         → *hoje
"tem algo urgente pra pausar?"    → *pausar
"atualiza os dados"               → *collect
"como tá a conta?"                → *status
"resumo de ontem"                 → *ontem
```

---

### FUNIL F1 / F2 / F3 — gestão operacional de criativos

```
*funil      │ Status de todas as campanhas classificadas por fase (F1/F2/F3/RMKT) com alertas
*f1         │ Laboratório — criativos em teste, CPA por dia, candidatos a corte
*f2         │ Arena — criativos ativos, quais pausar, quais subir para F3
*f3         │ Escala — ROAS sustentado? Frequência? Janela de 7 dias respeitada?
*mover      │ Ações do dia: o que promover (F1→F2, F2→F3) e o que pausar agora
*checklist  │ Checklist inteligente baseado no dia da semana (segunda/quarta/sexta)
```

Exemplos de ativação:
```
"quais criativos devo mover hoje?"        → *mover
"como tá o funil?"                        → *funil
"o que fazer hoje?"                       → *checklist
"quais criativos aprovados pra F2?"       → *f1
"tem alguém pra escalar na F3?"           → *f2
"a F3 tá sustentando?"                   → *f3
"segunda-feira, o que preciso fazer?"     → *checklist
```

---

### DIAGNÓSTICO — investigar um problema em profundidade

```
*criativos   │ Ranking completo de criativos por CPA — ALVO / BOM / LIMITE / CORTE / PAUSAR
*vsl         │ VSL A vs VSL B vs VSL C por produto — qual roteiro está ganhando
*reembolsos  │ Reembolsos por produto + por criativo via UTM + tendência diária
*checkout    │ Funil VPV -> IC -> Venda por produto com taxas e alertas automáticos
*fadiga      │ Criativos com frequência alta (>2.5x F3 / >3.0x F2) — risco de saturação
```

Exemplos de ativação:
```
"qual criativo tá com melhor CPA?"              → *criativos
"VSL A ou VSL C tá melhor?"                     → *vsl
"qual criativo tá gerando mais reembolso?"      → *reembolsos
"por que o checkout caiu?"                      → *checkout
"algum criativo saturando?"                     → *fadiga
"me mostra o ranking de ads"                    → *criativos
"qual roteiro escalar?"                         → *vsl
```

---

### VISÃO FINANCEIRA — rentabilidade real com reembolsos

```
*pl          │ P&L com receita REAL (VALOR PAGO) separando produto principal vs order bumps + reembolsos
*lucro       │ Lucro líquido real do período (alias de *pl)
*origem      │ Vendas por canal de origem: Facebook / Bio / Hotmart / Manychat / Comercial / Direto
*mes         │ Performance do mês atual consolidada por produto
*roi MDA     │ ROI isolado de um produto específico com análise detalhada
*budget      │ Distribuição do gasto entre F1/F2/F3/RMKT em % — quick_status.py --mode budget
```

Exemplos de ativação:
```
"pl março"                              → *pl março
"qual o lucro líquido da semana?"       → *lucro
"como tá o ROI do LVC?"                → *roi LVC
"quanto investi esse mês?"             → *mes
"como distribuir o budget?"            → *budget
"qual produto tá mais lucrativo?"      → *pl
"quanto perdi com reembolso?"          → *reembolsos + *pl
"quanto veio de orderbump?"            → *pl
"separa produto principal de bump"     → *pl
"de onde vêm as vendas?"              → *origem
"quanto vem do Facebook vs Hotmart?"  → *origem
"por que o checkout caiu?"            → *checkout
"qual a taxa IC->Venda?"              → *checkout
"qual a conversão do funil?"          → *checkout
```

---

### ANÁLISE COMPARATIVA — tendências e decisões de escala

```
*comparar              │ Semana atual vs semana anterior
*comparar março        │ Todas as semanas de março comparadas
*comparar fevereiro    │ Todas as semanas de fevereiro comparadas
*comparar sem-a sem-b  │ Duas semanas específicas (ex: *comparar 10/03 17/03)
*benchmarks            │ Período atual vs benchmarks históricos (fev/26)
*tendencia             │ Evolução de vendas e ROAS dos últimos 30 dias
```

Exemplos de ativação:
```
"como foi essa semana vs a anterior?"       → *comparar
"compara as semanas de março"               → *comparar março
"semana passada foi melhor ou pior?"        → *comparar
"o ROAS melhorou ou piorou?"               → *comparar
"compara fevereiro pra mim"                 → *comparar fevereiro
"qual foi a melhor semana do mês?"          → *comparar março
"tô acima ou abaixo do benchmark?"         → *benchmarks
```

---

### RELATÓRIOS E PIPELINE — documentação e análise completa

```
*report     │ Relatório Markdown completo — campanhas + criativos + P&L + ações prioritárias
*workflow   │ Pipeline completo: collect → validate → analyze-campaigns → analyze-creatives → report
*mensal     │ Relatório mensal — campeões, pausados, benchmark atualizado, planejamento do próximo mês
```

Exemplos de ativação:
```
"gera o relatório da semana"          → *report
"roda o workflow completo"            → *workflow
"fecha o mês"                         → *mensal
"quero o relatório completo"          → *report
"atualiza tudo e gera o report"       → *workflow
```

---

### Sintaxe de período — funciona com qualquer comando

```
*[comando] hoje                    → só hoje
*[comando] ontem                   → só ontem
*[comando] essa semana             → segunda até hoje
*[comando] semana passada          → semana anterior completa
*[comando] março / fevereiro       → mês por nome
*[comando] últimos 7 dias          → rolling 7 dias
*[comando] últimos 14 dias         → rolling 14 dias
*[comando] desde 10/03 até hoje    → intervalo customizado
```

---

### Regras de execução (obrigatórias)
1. Dados: sempre usar arquivo mais recente em `data/sheets/`
2. Desatualizado (> 1 dia): avisar, oferecer `*collect` e aguardar confirmação
3. Sempre ler `config/analyst-rules.md` antes de qualquer análise
4. Cruzar `diario_*` + `ads_*` + `reembolsos` — nunca análise parcial
5. Jamais inventar números — se dado ausente, informar claramente
6. Sempre revisar cálculos antes de publicar (ticket médio = R$ 184,23)

---

## Setup (once)

```bash
# 1. Copy credentials
cp .env.example .env
# Edit .env with your Meta API credentials

# 2. Install dependencies
pip install -r scripts/requirements.txt

# 3. Run pipeline (preset, custom range, or import)
python scripts/meta_collector.py --date-range yesterday
python scripts/meta_collector.py --since 2025-01-01 --until 2025-06-30
python scripts/data_importer.py --file export.csv --date-label 2025-01-15 --also-process
python scripts/data_processor.py --date $(date +%Y-%m-%d)
```

---

## Meta API Permissions Required

- `ads_read`
- `read_insights`
- `business_management`

---

*Synkra AIOS — Meta Ads Intelligence v1.1*
