# Audience Intelligence Guide — Regras de Qualidade e Segmentação de Audiência

> **Uso:** Referência para @analyst ao avaliar qualidade de audiência, detectar saturação e recomendar tipo de segmentação por fase do funil
> **Ref:** `docs/meta-knowledge/meta-03-audience-targeting.md`
> **Atualizado:** 2026-03-28

---

## 1. Detecção de Tipo de Audiência por Convenção de Nome

Como o sistema é read-only e não tem acesso direto às configurações de audiência, o tipo é inferido pelo nome da campanha/anúncio:

| Padrão no nome | Tipo de audiência inferido | Comportamento esperado |
|---|---|---|
| `RMKT` / `[Q]` | Custom Audience (visitantes, compradores, engajamento) | CPM baixo, ROAS alto, Frequência sobe rápido |
| `F1` | Tráfego frio — Detailed Targeting ou Broad | CPM variável, CPA alto inicialmente |
| `F2` / `F3` | Broad ou Lookalike (escala) | CPM estabiliza, CPA melhora com tempo |
| `ASC` | Advantage+ Audience (IA decide) | CPM otimizado automaticamente |
| `[F]` | Tráfego frio confirmado | Sem sobreposição com RMKT |
| Sem prefixo | Desconhecido | Pedir clarificação ao usuário |

---

## 2. Regras de Tamanho de Audiência

> ⚠️ O sistema não lê o tamanho da audiência diretamente dos CSVs. Estas regras são para @analyst aplicar ao revisar configurações no Ads Manager ou quando o usuário informar o tamanho.

### Thresholds por tipo de campanha

| Fase | Tamanho mínimo recomendado | Tamanho ideal | Alerta se menor que |
|------|---------------------------|---------------|---------------------|
| F1 — Laboratório (frio) | 500k pessoas | 1M–5M | 100k (muito restrita para teste) |
| F2 — Arena (escala) | 1M pessoas | 3M–10M | 500k |
| F3 — Escala total | 2M+ pessoas | 5M–20M | 1M |
| RMKT — Remarketing | 1.000 pessoas | 10k–500k | 500 (abaixo do Learning Phase) |
| Lookalike source (Custom Audience base) | 1.000 eventos | 5k–50k | 500 (qualidade de LLA cai muito) |

### Alertas de tamanho

**Audiência muito pequena (< 50k para tráfego frio):**
- CPM vai disparar — Meta leiloa o mesmo pool de pessoas repetidamente
- Frequência sobe rápido → fadiga acelerada
- Escala inviável — não tem volume para crescer o budget
- **Ação:** Expandir targeting, adicionar camadas de interesses, ou mudar para Advantage+ Audience

**Custom Audience de lista com < 1.000 pessoas:**
- Lookalike gerado a partir desta base terá baixa qualidade
- Meta não consegue encontrar padrões confiáveis em amostras pequenas
- **Ação:** Crescer a lista antes de criar Lookalike, ou usar engagement audience como alternativa

**Audiência muito grande (> 50M para F1):**
- Pode indicar targeting muito amplo sem relevância
- CPA pode ser alto por falta de qualificação
- **Ação:** Adicionar uma camada de qualificação (comportamento de compra, interesse específico)

---

## 3. Recomendações de Tipo de Audiência por Estágio do Funil

### Mapa de funil → audiência recomendada

| Estágio | Fase | Audiência Recomendada | Quando recomendar |
|---------|------|-----------------------|-------------------|
| **Topo (Prospecção)** | F1 | Detailed Targeting ou Broad | Sempre para F1 — testar qual targeting gera melhor CPA |
| **Topo (Escala)** | F2/F3 | Broad ou Lookalike 1-3% | Quando F1 tem CPA validado com histórico suficiente |
| **Automação total** | F2/F3 | Advantage+ Audience | Quando conta tem ≥ 100 conversões/semana |
| **Remarketing** | RMKT | Custom Audience (visitantes, compradores, engajamento) | Sempre para RMKT |
| **Prospecção com dados** | F2+ | Lookalike 1-3% de compradores | Quando Custom Audience de compradores tem ≥ 500 pessoas |

### Regra: Recomendar Lookalike quando:
1. Custom Audience de compradores ≥ **500 pessoas** (mínimo de qualidade)
2. Custom Audience de compradores ≥ **1.000 pessoas** (recomendado ideal)
3. Campanha já testou Detailed Targeting e tem CPA histórico de referência
4. **Percentual recomendado:** 1-3% para qualidade; 3-5% para volume

### Regra: Recomendar Broad/Advantage+ Audience quando:
1. Conta tem ≥ **100 conversões reais por semana** (pixel + conversions API)
2. Ou campanha F2/F3 com histórico de ≥ **30 dias** e CPA estável
3. O objetivo é **escalar** sem gestão intensiva de targeting
4. **Por quê:** Com dados suficientes, a IA da Meta é mais eficiente que targeting manual

### Regra: Evitar Lookalike alto (5-10%) para Sales:
- Lookalike 5-10% é muito amplo — perde a qualidade do sinal
- Para vendas, manter no máximo Lookalike 3% a menos que o volume exija

---

## 4. Sinais de Saturação de Audiência (Detecção via Métricas)

Como o sistema não lê o tamanho da audiência, a saturação é detectada por **sinais indiretos** nas métricas:

### Sinais primários de saturação

| Sinal | Threshold | Interpretação |
|-------|-----------|---------------|
| Frequência > 3.0x (F2) | 🔴 Alta | Audiência viu o mesmo anúncio 3+ vezes — fadiga |
| Frequência > 2.5x (F3) | 🟡 Alerta antecipado | Renovar criativos antes de saturar |
| CPM subindo > 20% em 7 dias | 🟡 Média | Meta pagando mais para alcançar o mesmo público — pool se esgotando |
| CTR caindo > 30% em 7 dias | 🟡 Média | Audiência já viu o anúncio — engajamento caindo |
| CPM subindo + CTR caindo simultaneamente | 🔴 Alta | Saturação confirmada — renovação urgente |

### Sinais secundários de saturação

| Sinal | Threshold | Ação |
|-------|-----------|------|
| CPA subindo sem mudança de criativo | > 20% em 7 dias | Investigar se é saturação ou sazonalidade |
| Alcance estagnado com spend estável | Alcance plano por 3+ dias | Audiência esgotada |
| VPV/Cliques caindo | < 60% por 3+ dias | Qualidade do tráfego deteriorando |

### Como calcular Frequência nos dados disponíveis

```python
# Em diario_*.csv — Frequência da CONTA (não por criativo)
frequencia_conta = impressoes_periodo / alcance_periodo

# Em ads_*.csv — Frequência por CRIATIVO não está disponível diretamente
# Proxy: CPM crescente + CTR decrescente = sinal de saturação no criativo
```

---

## 5. Detecção de Sobreposição de Audiências

### O problema da sobreposição

Quando múltiplos ad sets em F1 usam **os mesmos interesses**, eles competem entre si no leilão — inflando o CPM e dividindo o orçamento de forma ineficiente.

### Sinais de sobreposição via métricas

| Sinal | Interpretação |
|-------|---------------|
| CPM alto em F1 logo desde o início (dia 1-2) | Possível sobreposição entre ad sets ativos |
| Vários ad sets F1 com spend muito desigual (1 gasta 80%, outros 20%) | Meta concentrou em 1 porque os outros sobrepõem |
| CPA alto em todos os ad sets de F1 simultaneamente | Sobreposição inflando CPM da conta |

### Regra operacional para F1 anti-sobreposição

```
Estrutura ideal F1: 1 Campanha / X Conjuntos / 1 Criativo por Conjunto

Cada conjunto deve testar:
- Targeting diferente (interesses distintos) OU
- Criativo diferente com mesma audiência (A/B de criativo)

NÃO fazer:
- Múltiplos ad sets com mesmo conjunto de interesses
- Campanhas F1 de diferentes produtos com targeting idêntico rodando simultaneamente
```

### Como detectar sobreposição via nomes (quando aplicável)
- Se múltiplos `NOME ADS` têm nomes similares sem diferenciador de targeting → possível sobreposição
- Ex: `AD01 [MDA] VENDA - VSL A` e `AD02 [MDA] VENDA - VSL A` no mesmo período = mesmo criativo em conjuntos diferentes → verificar se audiências são distintas

---

## 6. Validação Funil × Tipo de Audiência

### Combinações inválidas a alertar

| Combinação | Alerta | Motivo |
|---|---|---|
| RMKT + Objetivo Awareness | 🔴 Conflito | Remarketing deve otimizar para conversão — awareness em quente desperdiça audiência |
| F1 tráfego frio + Custom Audience (lista de compradores) | 🟡 Verificar | Não é tráfego frio — é quente. Reclassificar como RMKT ou F1.5 |
| F3 escala + Audiência < 1M | 🔴 Problema | Não tem volume para escalar — CPM vai disparar |
| F2/F3 + Lookalike > 5% | 🟡 Subótimo | LLA muito ampla perde qualidade — considerar reduzir para 1-3% |
| ASC + Audiência manual muito restrita (audience suggestion muito específica) | 🟡 Problema | IA não consegue expandir — ver regras do advantage-plus-rules.md |

---

## 7. Recomendações por Volume de Conversões da Conta

A qualidade da otimização da Meta depende do volume de dados disponível:

| Conversões/semana (conta total) | Estratégia de audiência recomendada |
|----------------------------------|-------------------------------------|
| < 10 conversões/semana | Broad audience — não há dados suficientes para LLA ou Advantage+ funcionar bem |
| 10–50 conversões/semana | Detailed Targeting ou Lookalike 1% de lista existente |
| 50–100 conversões/semana | Lookalike 1-3% começa a funcionar bem; testar Advantage+ Audience |
| > 100 conversões/semana | Advantage+ Audience é a melhor opção; Broad também funciona |
| > 200 conversões/semana | Broad ou Advantage+ ideal; LLA desnecessário se Advantage+ entrega bem |

**Para esta conta (histórico fev/2026: ~499–694 vendas/semana):**
- Volume suficiente para Advantage+ Audience funcionar **muito bem**
- Lookalike de compradores de alta qualidade disponível
- Broad audience pode funcionar bem com histórico da conta

---

## 8. Checklist de Revisão de Audiência — Semanal

Aplicar ao revisar ad sets ativos no Ads Manager:

**Para F1:**
- [ ] Cada ad set tem targeting distinto dos demais (sem sobreposição)?
- [ ] Audiência estimada ≥ 500k?
- [ ] Não está usando Custom Audience de compradores (seria RMKT, não F1)?

**Para F2/F3:**
- [ ] Frequência ≤ 3.0x (F2) ou ≤ 2.5x (F3)?
- [ ] CPM está estável ou caindo (não subindo > 20% sem aumento de budget)?
- [ ] Audiência ≥ 1M (F2) ou ≥ 2M (F3)?

**Para RMKT:**
- [ ] Custom Audience tem ≥ 1.000 pessoas?
- [ ] Exclusões corretas (compradores excluídos de audiências de visitantes)?
- [ ] Frequência monitorada (remarketing satura mais rápido)?

**Para recomendar migração de targeting:**
- [ ] Conta tem ≥ 100 conversões/semana? → Advantage+ Audience
- [ ] Custom Audience de compradores tem ≥ 1.000 pessoas? → Criar Lookalike 1-3%
- [ ] F3 com audiência < 1M? → Expandir targeting urgente

---

## 9. Fontes

- `docs/meta-knowledge/meta-03-audience-targeting.md` — documentação base completa
- `config/analyst-rules.md` — Seções 3 (Alertas), 6 (Regras de análise)
- `docs/meta-knowledge/advantage-plus-rules.md` — Seção 3 (Advantage+ Audience)

---
*audience-intelligence-guide.md | Meta Ads Intelligence | 2026-03-28*
