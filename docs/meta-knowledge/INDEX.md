# Meta Knowledge Base — Índice

> Base de conhecimento oficial Meta Ads para o projeto **meta-ads-intelligence**
> Compilado de: Meta Blueprint, Meta Business Help Center, Advantage+ Docs, Bid Strategy Guide, Marketing API
> Referência: 2025-2026

---

## Arquivos Disponíveis

| Arquivo | Conteúdo | Linhas | Quando usar |
|---------|----------|--------|-------------|
| [meta-01-blueprint-courses.md](meta-01-blueprint-courses.md) | Cursos Blueprint, trilhas de aprendizado, certificações, conceitos-chave | 432 | Entender o que a Meta ensina como padrão; verificar conceitos fundamentais |
| [meta-02-campaign-structure.md](meta-02-campaign-structure.md) | Hierarquia Campaign→AdSet→Ad, 6 objetivos, CBO vs ABO, leilão, formatos | 625 | Analisar estrutura de campanha; validar objetivo vs otimização; entender o leilão |
| [meta-03-audience-targeting.md](meta-03-audience-targeting.md) | Core/Custom/Lookalike/Advantage+ Audience, detailed targeting, retargeting, funil | 616 | Avaliar qualidade de audiência; recomendar tipo de segmentação; estratégia de funil |
| [meta-04-advantage-plus.md](meta-04-advantage-plus.md) | Suite Advantage+ completa (ASC, audience, placements, creative, catalog), migração | 797 | Analisar campanhas Advantage+; recomendar migração; benchmarks de automação |
| [meta-05-bidding-attribution.md](meta-05-bidding-attribution.md) | Estratégias de lance, janelas de atribuição, métricas, Pixel/CAPI, benchmarks | 1150 | Avaliar estratégia de lance; interpretar métricas; contextualizar ROAS por atribuição |

**Total:** 3.620 linhas de documentação oficial compilada

---

## Guia de Uso por Caso

### "Qual objetivo de campanha usar?"
→ `meta-02-campaign-structure.md` — Seção 2 (Os 6 Objetivos)

### "Como avaliar a audiência desta campanha?"
→ `meta-03-audience-targeting.md` — Seção 8 (Tamanhos Recomendados) + Seção 6 (Estratégia de Funil)

### "Esta campanha Advantage+ está bem configurada?"
→ `meta-04-advantage-plus.md` — Seção 2 (ASC) ou Seção 3 (Advantage+ Audience)

### "O ROAS reportado é confiável?"
→ `meta-05-bidding-attribution.md` — Seção 3 (Janelas de Atribuição)

### "Qual estratégia de lance usar?"
→ `meta-05-bidding-attribution.md` — Seção 1 (Estratégias de Lance) + Tabela de seleção

### "Como funciona o leilão da Meta?"
→ `meta-02-campaign-structure.md` — Seção 4 (O Leilão de Anúncios Meta)

### "Devo migrar para Advantage+?"
→ `meta-04-advantage-plus.md` — Seção 8 (Advantage+ vs Manual) + Seção 9 (Migração)

### "Quais métricas acompanhar?"
→ `meta-05-bidding-attribution.md` — Seção 4 (Glossário de Métricas) + Seção 6 (Benchmarks)

---

## Destaque: Descobertas Críticas

### ⚠️ Advantage+ dobrou custo de novo cliente em 2025
Análise independente de 55.661 campanhas (Wicked Reports) mostrou que o nCAC (new customer acquisition cost) com Advantage+ foi de $257 → $528 entre 2024-2025. Estratégia recomendada: **híbrida** — Advantage+ para retargeting/bottom-of-funnel, manual para topo de funil.
> Ver: `meta-04-advantage-plus.md` — Seção 8

### ⚠️ Janela de atribuição 7-day view foi depreciada em Jan/2026
A janela `7-day view` foi removida em 12/01/2026. Janelas ativas: 1-day click, 7-day click, 1-day view, 1-day engaged view.
> Ver: `meta-05-bidding-attribution.md` — Seção 3

### ✅ Orçamento lifetime sai da Learning Phase 18% mais rápido
Pesquisa 2025 indica que orçamentos vitalícios têm vantagem na fase de aprendizado.
> Ver: `meta-05-bidding-attribution.md` — Seção 2

---

## Relação com Stories

| Story | Usa estes arquivos |
|-------|-------------------|
| [2.1 — Setup KB](../stories/story-2.1-meta-knowledge-base-setup.md) | Todos (criação) |
| [2.2 — Analyst Rules Alignment](../stories/story-2.2-analyst-rules-alignment.md) | meta-02, meta-03, meta-04, meta-05 |
| [2.3 — Advantage+ Tracking](../stories/story-2.3-advantage-plus-tracking.md) | meta-04 principalmente |
| [2.4 — Bidding & Attribution](../stories/story-2.4-bidding-attribution-rules.md) | meta-05 principalmente |
| [2.5 — Audience Intelligence](../stories/story-2.5-audience-segmentation-rules.md) | meta-03 principalmente |

---
*Gerado em 2026-03-28 | meta-ads-intelligence v1.2.2+*
