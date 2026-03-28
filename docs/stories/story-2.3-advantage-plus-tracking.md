# Story 2.3 — Advantage+ Tracking: Análise e Recomendações

**Epic:** Meta Knowledge Base Integration
**Status:** Done
**Priority:** Medium
**Estimativa:** 3h

---

## Contexto

A Meta está migrando agressivamente para campanhas Advantage+ (ASC, Advantage+ Audience, etc.). O meta-ads-intelligence atualmente não tem regras específicas para diferenciar, avaliar e recomendar Advantage+ vs campanhas manuais.

Com a documentação oficial compilada em `meta-04-advantage-plus.md`, esta story implementa suporte completo ao ecossistema Advantage+ no sistema de análise.

## Objetivo

Adicionar ao meta-ads-intelligence a capacidade de:
1. Identificar se uma campanha é Advantage+ ou manual
2. Aplicar critérios de avaliação corretos para cada tipo
3. Recomendar migração para Advantage+ quando apropriado
4. Alertar sobre configurações subótimas em campanhas Advantage+

## Acceptance Criteria

- [x] Sistema consegue identificar tipo de campanha: ASC, ADV+, RMKT, MANUAL (via `tipo_criativo()` em `analyze_creatives_v2.py`)
- [x] Regras de avaliação ajustadas por tipo (14 dias para ASC vs 7 dias manual, thresholds documentados)
- [x] Nova regra: recomendar ASC quando ≥50 conversões/semana + ROAS ≥2.5x sustentado (`advantage-plus-rules.md` Seção 5)
- [x] Nova regra: alertar quando Advantage+ Audience com audience suggestions restritivas (`advantage-plus-rules.md` Seção 3)
- [x] Nova regra: identificar uso incorreto de Advantage+ Creative (`advantage-plus-rules.md` Seção 4)
- [x] Templates `daily-report-tmpl.md` e `weekly-summary-tmpl.md` atualizados com coluna Tipo + legenda
- [x] `docs/meta-knowledge/advantage-plus-rules.md` criado (8 seções)

## Tarefas

- [x] Ler `meta-04-advantage-plus.md` e mapear critérios de avaliação
- [x] Identificar campos nos dados de entrada que indicam tipo Advantage+ (NOME ADS com prefixo ASC/ADV+)
- [x] Implementar detecção: `tipo_criativo()` e `campaign_type_label()` em `analyze_creatives_v2.py`
- [x] Criar regras de avaliação específicas para ASC (Seção 2 do advantage-plus-rules.md)
- [x] Criar regras de avaliação para Advantage+ Audience (Seção 3)
- [x] Criar regras de recomendação de migração (Seção 5)
- [x] Atualizar templates de relatório (coluna Tipo adicionada em ambos)
- [x] Documentar em advantage-plus-rules.md
- [ ] Testar com dados reais (validar que prefixo ASC aparece nos NOME ADS reais)

## File List

- `config/analyst-rules/advantage-plus-rules.md` (novo)
- `docs/meta-knowledge/advantage-plus-rules.md` (novo)
- `scripts/analyze_creatives_v2.py` (modificação — detecção de tipo)
- `templates/*.md` (modificação — label Advantage+)

## Dependências

- **Requer:** Story 2.1 completa
- **Relacionada:** Story 2.2 (alinhamento geral de regras)

---
*Story criada em 2026-03-28 | Epic: Meta Knowledge Base Integration*
