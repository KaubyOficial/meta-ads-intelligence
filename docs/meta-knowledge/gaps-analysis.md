# Gaps Analysis — analyst-rules vs Documentação Oficial Meta

> Gerado em: 2026-03-28
> Base de comparação: `config/analyst-rules.md` (v2026-03-20) vs `docs/meta-knowledge/` (compilado de fontes oficiais Meta 2025-2026)
> Status: **Gaps de alta prioridade implementados na Story 2.2**

---

## Resumo

| Prioridade | Gap | Status |
|-----------|-----|--------|
| 🔴 Alta | Campanhas ASC sem regras de avaliação | ✅ Implementado — Seção 12 |
| 🔴 Alta | Learning Phase ignorada nas regras de F1 | ✅ Implementado — Seção 13 |
| 🔴 Alta | Janela de atribuição não definida | ✅ Implementado — Seção 14 |
| 🟡 Média | Nenhuma referência aos arquivos meta-knowledge | ✅ Implementado — Seção 9 |
| 🟡 Média | Nenhuma regra para Advantage+ Audience em campanhas manuais | Backlog — Story 2.5 |
| 🟡 Média | Estratégia de lance não documentada (qual bid strategy usar por fase) | Backlog — Story 2.4 |
| 🟡 Média | Nenhuma regra de audience quality/overlap | Backlog — Story 2.5 |
| 🟢 Baixa | Benchmarks de CTR/CPM não atualizados com dados de indústria 2025 | Backlog — account-benchmarks.md |
| 🟢 Baixa | Reels ads não mencionados como formato prioritário | Backlog |
| 🟢 Baixa | Nenhuma regra para Click-to-Message/WhatsApp ads | Fora do escopo atual |

---

## Gaps Implementados (Story 2.2)

### Gap 1: Campanhas ASC sem regras de avaliação
**Problema:** A Seção 4 do analyst-rules tinha `ASC` como prefixo de campanha mas **zero critérios** de como avaliá-las. Campanhas ASC foram tratadas implicitamente como campanhas manuais, o que é incorreto.

**O que a Meta diz:**
- ASC precisa de 50+ compras/semana na conta para funcionar bem
- Período mínimo de leitura é 14 dias (não 7 como campanhas manuais)
- Frequência alta em ASC pode ser intencional — Meta gerencia a audiência
- Descoberta crítica independente (2025): nCAC dobrou com ASC vs manual ($257→$528) para aquisição de novos clientes

**Implementação:** `config/analyst-rules.md` — Seção 12 adicionada com tabela de critérios, alertas e regras de "não fazer".

---

### Gap 2: Learning Phase ignorada nas regras de F1
**Problema:** As regras diziam "F1 com < 3 dias: não tomar decisão de corte — apenas monitorar CPM" mas nunca explicavam por quê, nem o impacto de F1 operar permanentemente em Learning Limited.

**O que a Meta diz:**
- 50 eventos de otimização/semana por ad set = requisito para sair do Learning Phase
- Ad sets em Learning Limited têm entrega instável e CPA artificialmente alto
- F1 a R$50/dia com CPA médio de ~R$130 gera apenas ~2-3 conversões/semana (longe das 50 necessárias)

**Impacto na conta:** Todo F1 desta conta opera em Learning Limited permanente. Isso é aceitável para um laboratório de testes, mas as regras devem reconhecer isso para evitar descartar criativos válidos por instabilidade de learning.

**Implementação:** `config/analyst-rules.md` — Seção 13 adicionada com tabela de impacto, sinais válidos mesmo em Learning Limited e distinção F1 vs F2/F3.

---

### Gap 3: Janela de atribuição nunca definida
**Problema:** A Seção 8 dizia "sempre incluir nota sobre janela de atribuição" mas **nunca definia qual janela a conta usa** nem como interpretar dados em diferentes janelas.

**O que a Meta diz:**
- 7-day view foi depreciada em 12/01/2026 — não está mais disponível
- Janelas disponíveis: 1-day click, 7-day click, 1-day view, 1-day engaged view
- Diferentes janelas produzem ROAS incomparáveis entre si

**Impacto na conta:** Dados de `data/processed/` (Meta API) e `vendas_*.csv` (Hotmart) divergem por design — a janela de atribuição explica parte disso. Sem essa definição, analistas podem confundir as fontes.

**Implementação:** `config/analyst-rules.md` — Seção 14 adicionada com janela padrão definida (7-day click), impacto por janela, e regras de interpretação incluindo iOS 14+ e divergência típica Pixel vs fonte real (60-80%).

---

## Gaps Pendentes (Backlog)

### Gap 4: Advantage+ Audience em campanhas manuais
**Problema:** As campanhas F1/F2/F3 podem usar Advantage+ Audience (expansão de audiência por IA) em vez de segmentação detalhada. As regras atuais não diferenciam nem avaliam esse targeting.

**Impacto esperado:** Médio — afeta qualidade da análise de audiência por fase.
**Story:** 2.5 — Audience Intelligence
**Ref:** `docs/meta-knowledge/meta-03-audience-targeting.md` — Seção 5

---

### Gap 5: Estratégia de lance não documentada
**Problema:** As regras não documentam qual bid strategy cada fase usa (Lowest Cost? Cost Cap?). Isso importa para interpretar CPA volátil — Cost Cap pode **underdelivar** quando o cap está muito baixo, enquanto Lowest Cost gasta o orçamento mas com CPA variável.

**Impacto esperado:** Médio — especialmente para F3 onde o bid strategy pode ser o motivo de underspend.
**Story:** 2.4 — Bidding & Attribution
**Ref:** `docs/meta-knowledge/meta-05-bidding-attribution.md` — Seção 1

---

### Gap 6: Audience quality e overlap
**Problema:** Sem regras para detectar quando audiências de F1 são muito pequenas (<50k) ou quando há sobreposição entre ad sets, causando canibalização.

**Impacto esperado:** Médio — especialmente em campanhas com muitos ad sets F1 simultâneos.
**Story:** 2.5 — Audience Intelligence
**Ref:** `docs/meta-knowledge/meta-03-audience-targeting.md` — Seção 7

---

### Gap 7: Benchmarks de CTR/CPM de indústria
**Problema:** O alerta de "CTR baixo < 0.5%" na Seção 3 não tem base documentada. O benchmark 2025 para infoprodutos/cursos online (Education) é CTR ~1.0-1.5% (Feed) e CPM ~R$15-40.

**Impacto esperado:** Baixo — os números atuais são conservadores e funcionam na prática.
**Ação:** Atualizar `config/account-benchmarks.md` com dados de indústria.

---

### Gap 8: Reels como formato prioritário
**Problema:** As regras de criativo não mencionam Reels como formato prioritário da Meta em 2025-2026. Meta está priorizando entrega de Reels e Stories em detrimento do Feed.

**Impacto esperado:** Baixo — impacta estratégia criativa, não análise de performance diretamente.
**Ação:** Adicionar nota sobre formatos na Seção 7 ou 8.

---

## Terminologia: Alinhamento com Meta Oficial

| Termo anterior nas regras | Termo oficial Meta | Status |
|---|---|---|
| "Campanha de vendas" | Campaign Objective: **Sales** | ✅ Consistente (Seção 1) |
| "Público" (informal) | **Audience** ou **Ad Set** | 🟡 Pode ser mais preciso |
| "Orçamento por campanha" | **Campaign Budget Optimization (CBO)** | ✅ Já usa CBO |
| "Orçamento por conjunto" | **Ad Set Budget Optimization (ABO)** | ✅ Já usa ABO |
| "Fase de aprendizado" | **Learning Phase** / **Learning Limited** | ✅ Seção 13 agora usa terminologia oficial |
| "Campanha automática" | **Advantage+ Shopping Campaign (ASC)** | ✅ Seção 12 agora usa terminologia oficial |
| "Janela de conversão" | **Attribution Window** | ✅ Seção 14 agora define corretamente |

---

*Gaps-analysis.md criado em 2026-03-28 | Story 2.2 | Meta Ads Intelligence*
