# Story 2.4 — Bidding & Attribution: Regras de Lance e Janelas de Atribuição

**Epic:** Meta Knowledge Base Integration
**Status:** Done
**Priority:** Medium
**Estimativa:** 2h

---

## Contexto

A interpretação correta de métricas no Meta Ads depende criticamente da estratégia de lance e da janela de atribuição configurada. Um ROAS de 3x com janela 7d click é fundamentalmente diferente de um ROAS de 3x com janela 1d click.

O meta-ads-intelligence atualmente não considera janela de atribuição nem valida se a estratégia de lance está adequada ao objetivo da campanha.

## Objetivo

Implementar no sistema de análise:
1. Validação de estratégia de lance por objetivo de campanha
2. Alertas sobre janela de atribuição e impacto nos números
3. Recomendações de lance baseadas em maturidade da campanha
4. Glossário de métricas com contexto de interpretação correto

## Acceptance Criteria

- [x] Nova regra: mapa bid strategy × fase (Seção 15 do analyst-rules.md + bidding-attribution-guide.md Seção 1)
- [x] Nova regra: alerta janela não definida + checklist de atribuição (`bidding-attribution-guide.md` Seção 7)
- [x] Nova regra: recomendar Cost Cap quando CPA volátil (Seção 15 do analyst-rules.md)
- [x] Nova regra: alerta underspend/Bid Cap restritivo < 80% do orçamento (Seção 15)
- [x] ROAS ajustado por janela (bidding-attribution-guide.md Seção 4 — tabela 1d click vs 7d click)
- [x] Seção "Contexto de Atribuição" adicionada aos dois templates
- [x] `docs/meta-knowledge/bidding-attribution-guide.md` criado (10 seções)

## Tarefas

- [x] Ler `meta-05-bidding-attribution.md` e mapear compatibilidades
- [x] Mapear janela de atribuição nos dados (7-day click = padrão; ads_*.csv usa Pixel)
- [x] Implementar validação lance × fase (Seção 15 + guia)
- [x] Implementar alertas de janela e divergência Pixel vs vendas_*.csv
- [x] Ajustar thresholds ROAS por janela (Seção 4 do guia)
- [x] Regras de Cost Cap e underspend implementadas
- [x] Templates atualizados com seção Contexto de Atribuição
- [x] Documentação criada e completa

## File List

- `config/analyst-rules/bidding-rules.md` (novo ou modificação)
- `docs/meta-knowledge/bidding-attribution-guide.md` (novo)
- `scripts/analyze_creatives_v2.py` (modificação)
- `templates/*.md` (modificação)

## Dependências

- **Requer:** Story 2.1 completa
- **Relacionada:** Story 2.2 (alinhamento geral)

---
*Story criada em 2026-03-28 | Epic: Meta Knowledge Base Integration*
