# Story 2.2 — Analyst Rules: Alinhamento com Documentação Oficial Meta

**Epic:** Meta Knowledge Base Integration
**Status:** Done
**Priority:** High
**Estimativa:** 3h

---

## Contexto

Com os 5 arquivos de conhecimento oficial criados na Story 2.1, esta story revisa e atualiza as `analyst-rules` do meta-ads-intelligence para garantir alinhamento com as melhores práticas e nomenclatura oficial da Meta.

Atualmente as regras podem usar terminologia informal ou critérios baseados apenas em experiência. O objetivo é ancorar cada regra na documentação oficial.

## Objetivo

Revisar todos os arquivos de regras do analyst (`config/analyst-rules/`) e:
1. Alinhar nomenclatura com os termos oficiais Meta
2. Adicionar referências aos arquivos `meta-knowledge/` relevantes
3. Identificar gaps — regras que deveriam existir mas não existem
4. Criar novas regras baseadas em best practices identificadas na KB oficial

## Acceptance Criteria

- [x] Todos os arquivos em `config/analyst-rules/` revisados
- [x] Terminologia alinhada com nomenclatura oficial Meta (Learning Phase, ASC, Attribution Window, CBO/ABO)
- [x] Cada regra principal tem referência ao arquivo meta-knowledge/ correspondente (Seção 9 atualizada)
- [x] Lista de gaps identificados documentada em `docs/meta-knowledge/gaps-analysis.md`
- [x] Novas regras criadas para gaps de alta prioridade (3 novas seções: 12, 13, 14)
- [x] Regras existentes não quebradas — seções 1-11 mantidas intactas

## Tarefas

- [x] Ler todos os arquivos em `config/analyst-rules/`
- [x] Comparar com `meta-02-campaign-structure.md` — Learning Phase identificada como gap crítico
- [x] Comparar com `meta-03-audience-targeting.md` — gap de audience quality documentado no backlog
- [x] Comparar com `meta-04-advantage-plus.md` — Seção 12 (ASC rules) implementada
- [x] Comparar com `meta-05-bidding-attribution.md` — Seção 14 (attribution window) implementada
- [x] Documentar gaps em `gaps-analysis.md`
- [x] Implementar novas regras prioritárias (Seções 12, 13, 14)
- [x] Validar que análises existentes continuam funcionando (seções 1-11 preservadas)

## File List

- `config/analyst-rules/*.md` (modificações)
- `docs/meta-knowledge/gaps-analysis.md` (novo)

## Dependências

- **Requer:** Story 2.1 completa (arquivos meta-knowledge/ existentes)

---
*Story criada em 2026-03-28 | Epic: Meta Knowledge Base Integration*
