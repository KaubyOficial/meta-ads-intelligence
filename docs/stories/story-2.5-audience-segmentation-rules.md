# Story 2.5 — Audience Intelligence: Regras de Segmentação e Qualidade de Audiência

**Epic:** Meta Knowledge Base Integration
**Status:** Done
**Priority:** Medium
**Estimativa:** 3h

---

## Contexto

A qualidade e o tipo de audiência impactam diretamente o desempenho das campanhas. Audiências muito pequenas, muito amplas, sobrepostas ou com tipo errado para o objetivo são causas comuns de performance fraca.

Com a base de conhecimento oficial compilada em `meta-03-audience-targeting.md`, esta story implementa regras de análise de audiência no sistema.

## Objetivo

Adicionar ao meta-ads-intelligence a capacidade de:
1. Avaliar a qualidade e adequação da audiência para o objetivo
2. Detectar audiências sobrepostas entre ad sets
3. Recomendar tipo de audiência (Custom, Lookalike, Broad, Advantage+) por estágio do funil
4. Alertar sobre audiências muito pequenas ou muito grandes

## Acceptance Criteria

- [x] Nova regra: alertar audiência < 50k tráfego frio (audience-intelligence-guide.md Seção 2 + analyst-rules Seção 16)
- [x] Nova regra: alertar Custom Audience < 1.000 pessoas (Seção 2 + Seção 16)
- [x] Nova regra: recomendar Lookalike 1-3% quando compradores ≥ 1.000 (Seção 3)
- [x] Nova regra: recomendar Advantage+ Audience quando conta tem ≥ 100 conversões/semana (Seção 3 + Seção 7)
- [x] Nova regra: detectar sobreposição via sinais de CPM alto no início (Seção 5)
- [x] Nova regra: validar funil × tipo de audiência — tabela de combinações inválidas (Seção 6)
- [x] Seção "Análise de Audiência" adicionada em daily-report-tmpl.md e weekly-summary-tmpl.md
- [x] `docs/meta-knowledge/audience-intelligence-guide.md` criado (9 seções)

## Tarefas

- [x] Ler `meta-03-audience-targeting.md` e mapear critérios
- [x] Identificar campos disponíveis: tipo inferido por nome; saturação via CPM+CTR dos ads_*.csv
- [x] Implementar detecção de tipo de audiência por prefixo (analyst-rules Seção 16)
- [x] Implementar regras de tamanho mínimo/máximo (Seção 2 do guia)
- [x] Documentar sinais de sobreposição (Seção 5 do guia)
- [x] Recomendações por estágio de funil implementadas (Seção 3 do guia)
- [x] `saturation_signal()` adicionada ao analyze_creatives_v2.py — detecta CPM alto + CTR baixo
- [x] Bloco "ALERTAS DE AUDIÊNCIA / SATURAÇÃO" adicionado ao output do script
- [x] Templates atualizados com tabela de análise de audiência

## File List

- `config/analyst-rules/audience-rules.md` (novo)
- `docs/meta-knowledge/audience-intelligence-guide.md` (novo)
- `scripts/analyze_creatives_v2.py` (modificação)
- `templates/*.md` (modificação)

## Dependências

- **Requer:** Story 2.1 completa
- **Relacionada:** Stories 2.2, 2.3, 2.4

## Notas

Esta story pode ser dividida em 2 partes se o escopo for grande:
- 2.5a — Regras de tamanho e tipo de audiência
- 2.5b — Detecção de sobreposição e recomendações de funil

---
*Story criada em 2026-03-28 | Epic: Meta Knowledge Base Integration*
