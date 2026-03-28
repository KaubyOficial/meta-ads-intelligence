# Advantage+ Rules — Regras Operacionais para Campanhas Meta Advantage+

> **Uso:** Referência operacional para @analyst ao analisar campanhas com prefixo ASC ou que usem Advantage+ Audience/Creative
> **Ref:** `docs/meta-knowledge/meta-04-advantage-plus.md`
> **Atualizado:** 2026-03-28

---

## 1. Detecção de Tipo de Campanha

### Como identificar uma campanha Advantage+

| Padrão no nome | Tipo | Tratamento |
|---|---|---|
| Prefixo `ASC` | Advantage+ Sales Campaign (automação total) | Aplicar regras Seção 2 |
| Contém `[ADV+]` ou `ADVANTAGE` | Advantage+ Audience em campanha manual | Aplicar regras Seção 3 |
| Prefixo `F1`, `F2`, `F3` | Campanha manual (funil padrão) | Aplicar regras Seções 2–6 de analyst-rules.md |
| Prefixo `RMKT` ou `[Q]` | Remarketing manual | Regras padrão RMKT |
| Prefixo `F0` | Engajamento/aquecimento | Objetivo diferente — não avaliar por CPA de venda |

> Se o prefixo não for identificável, classificar como `MANUAL/DESCONHECIDO` e alertar no relatório.

---

## 2. Regras de Avaliação — ASC (Advantage+ Sales Campaigns)

### Pré-requisitos para ASC funcionar bem
- ≥ **50 compras/semana na conta** (total, não só na campanha ASC)
- Orçamento mínimo recomendado: **R$ 500/dia**
- Pelo menos **150 criativos** no banco de dados (Meta recombina automaticamente)

### Período mínimo antes de avaliar
- **14 dias** de dados antes de qualquer decisão estratégica
- Nos primeiros 7 dias: apenas monitorar entrega e CPA tendência — não cortar

### Thresholds de avaliação ASC

| Métrica | Threshold | Ação |
|---------|-----------|------|
| ROAS após 14 dias | < 2.0x | Revisão crítica — pausar e analisar criativos |
| ROAS após 14 dias | ≥ 2.0x < 3.0x | Manter — monitorar semanalmente |
| ROAS após 14 dias | ≥ 3.0x | Ótimo — priorizar renovação de criativos |
| CPA após 14 dias | > R$ 163,42 | Revisar criativos — não mexer em orçamento ainda |
| CPA após 14 dias | R$ 108,94–163,42 | Manter — ASC precisa de tempo |
| CPA após 14 dias | ≤ R$ 108,94 | Excelente — considerar aumentar orçamento |
| Entrega | < 80% do orçamento | Verificar se bid cap está muito restritivo |

### ⚠️ Alerta crítico: ASC e custo de novo cliente
Pesquisa independente com 55.661 campanhas (2025) mostrou que **nCAC (new customer acquisition cost) dobrou** com ASC vs campanhas manuais ($257 → $528). ASC tende a reciclar audiências já convertidas (retargeting implícito), inflando o ROAS mas encarecendo novos clientes.

**Regra operacional:**
- ✅ ASC para: escala de remarketing, reativação de base, bottom-of-funnel
- ❌ ASC para: aquisição pura de novos clientes (usar F1/F2/F3 manual)
- Ao comparar ASC vs F3: não comparar ROAS direto — ASC pode ter ROAS mais alto por trabalhar audiências mais quentes

### O que NÃO fazer com ASC

| Ação proibida | Por quê |
|---|---|
| Pausar e reativar ASC frequentemente | Reseta o aprendizado de IA — perde dados de otimização |
| Criar múltiplas ASC para o mesmo produto | Canibalização — as campanhas competem entre si no leilão |
| Avaliar ASC nos primeiros 7 dias | Instabilidade de learning — dados não confiáveis |
| Comparar ASC com F1 | Objetivos diferentes — ASC não é laboratório de criativos |
| Mexer em orçamento ASC < 7 dias de intervalo | Mesma regra da janela que campanhas manuais |

---

## 3. Regras de Avaliação — Advantage+ Audience em Campanhas Manuais

Campanhas F1/F2/F3 podem usar **Advantage+ Audience** (expansão por IA) em vez de segmentação detalhada manual.

### Como detectar
- Campo de targeting do ad set não tem interesses/comportamentos específicos definidos
- Meta expandiu automaticamente além da audiência sugerida
- Na análise: se CPM está muito baixo e alcance muito amplo para o orçamento → possível Advantage+ Audience ativo

### Regras de avaliação

| Cenário | Ação recomendada |
|---------|-----------------|
| F1 com Advantage+ Audience + CPA ≤ BOM (R$108,94) | Excelente — sinal que a IA encontrou audiência qualificada. Manter. |
| F1 com Advantage+ Audience + CPA > LIMITE (R$130,73) em 5+ dias | Restringir audiência — adicionar audience suggestions mais específicas |
| F2/F3 com Advantage+ Audience + frequência > 3.0x | Paradoxo: IA pode estar saturando um segmento. Revisar se audience suggestions estão muito restritas. |
| F2/F3 com Advantage+ Audience + ROAS ≥ 3.0x | Ideal — deixar rodar sem interferência |

### ⚠️ Alerta: Audience Suggestions muito restritivas
Se Advantage+ Audience está com **audience suggestions** (hints) muito específicas (ex: interesses muito nichados), a IA fica "presa" e não consegue expandir adequadamente.
- **Sinal:** CPM alto + alcance baixo para o orçamento
- **Ação:** Ampliar ou remover audience suggestions — deixar a IA agir com mais liberdade

---

## 4. Regras de Avaliação — Advantage+ Creative

### O que o Advantage+ Creative faz automaticamente
- Ajusta brilho, contraste e saturação da imagem
- Adiciona música de fundo em vídeos (se habilitado)
- Aplica templates de imagem
- Adiciona motion 3D em imagens estáticas
- Testa variações de texto (headline, descrição)

### Quando alertar sobre uso incorreto

| Situação | Alerta | Ação |
|----------|--------|------|
| Campanha de produto premium com Advantage+ Creative ativo | 🟡 Verificar | Ajustes automáticos de brilho/contraste podem distorcer identidade visual. Revisar se está afetando a marca. |
| CTR caiu após ativar Advantage+ Creative | 🔴 Investigar | Pode ser que as variações auto-geradas estejam performando pior. Desabilitar temporariamente para teste A/B. |
| CPA piorou após ativar Advantage+ Creative | 🔴 Desabilitar | Reverter para criativos originais e comparar por 7 dias. |
| VSL (vídeo longo) com Advantage+ Creative ativo | 🟡 Cautela | Meta pode cortar o início do vídeo ou adicionar elementos que interferem no hook. Verificar prévia do anúncio. |
| Advantage+ Creative DESABILITADO em campanha de imagem simples com baixo CTR | 🟢 Recomendar ativar | A IA pode melhorar performance de imagens estáticas com baixo engajamento. |

---

## 5. Regra de Recomendação de Migração para ASC

### Quando recomendar ASC
Recomendar migração de campanha manual para ASC quando **TODAS** as condições forem verdadeiras:

1. Campanha de objetivo **Sales** (Vendas)
2. Conta tem **≥ 50 compras reais/semana** no total
3. A campanha manual está há **≥ 30 dias** rodando
4. ROAS sustentado ≥ 2.5x nos últimos 14 dias
5. O anunciante quer **escalar** sem gestão manual intensiva

### Quando NÃO recomendar ASC
- Conta com < 50 compras/semana total
- Orçamento disponível < R$ 500/dia
- O objetivo é testar criativos novos (usar F1)
- Produto com ciclo de venda longo (>7 dias) — ASC precisa de conversões rápidas
- Conta nova (< 3 meses de histórico)

---

## 6. Label de Identificação no Relatório

Ao gerar relatório, campanhas Advantage+ devem ter label explícito:

```
[ASC]         → Advantage+ Sales Campaign (automação total)
[ADV+ AUD]    → Advantage+ Audience (manual + expansão IA)
[ADV+ CRTV]   → Advantage+ Creative ativo
[MANUAL]      → Campanha totalmente manual (F1/F2/F3)
```

**Exemplo de linha de relatório:**
```
| ASC-MDA-MARÇO | [ASC] | R$ 1.200/dia | ROAS 3.2x | 14d | ✅ Dentro do threshold |
```

---

## 7. Campo `rules_applied` para campanhas Advantage+

Ao analisar campanhas ASC ou com Advantage+, adicionar ao artifact:

```json
"rules_applied": [
  "advantage-plus-rules",
  "asc-14day-minimum",
  "cpa-targets-r196",
  "janela-7-dias-orcamento"
]
```

---

## 8. Fontes

- `docs/meta-knowledge/meta-04-advantage-plus.md` — documentação base completa
- `config/analyst-rules.md` — Seção 12 (regras integradas ao sistema principal)
- Pesquisa Wicked Reports: 55.661 campanhas analisadas, nCAC Advantage+ 2024→2025

---
*advantage-plus-rules.md | Meta Ads Intelligence | 2026-03-28*
