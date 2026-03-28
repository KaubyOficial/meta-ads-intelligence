# Bidding & Attribution Guide — Regras Operacionais de Lance e Atribuição

> **Uso:** Referência para @analyst ao interpretar métricas, recomendar estratégias de lance e contextualizar janelas de atribuição
> **Ref:** `docs/meta-knowledge/meta-05-bidding-attribution.md`
> **Atualizado:** 2026-03-28

---

## 1. Estratégias de Lance — Compatibilidade por Fase

### Mapa de compatibilidade: Fase × Bid Strategy recomendada

| Fase | Bid Strategy recomendada | Por quê | Evitar |
|------|--------------------------|---------|--------|
| **F1 — Laboratório** | **Lowest Cost** (sem restrição) | F1 precisa de entrega máxima para testar criativos. Restrições de lance causam underspend e dados insuficientes. | Cost Cap, Bid Cap, Minimum ROAS |
| **F2 — Arena** | **Lowest Cost** ou **Cost Cap** | Lowest Cost para escalar; Cost Cap quando CPA está volátil e se quer estabilizar entorno de R$130 | Bid Cap muito agressivo |
| **F3 — Escala** | **Cost Cap** ou **Lowest Cost** | Cost Cap garante previsibilidade no CPA ao escalar; Lowest Cost se confia no histórico da campanha | Minimum ROAS (pode causar underspend com target alto) |
| **ASC** | **Lowest Cost** (padrão ASC) | ASC gerencia lances internamente — não é possível definir Bid Cap em ASC. Não interferir. | Qualquer restrição manual (ASC é automático) |
| **RMKT** | **Lowest Cost** ou **Minimum ROAS** | Audiências quentes convertem bem — Minimum ROAS pode funcionar se CPA histórico for estável | Bid Cap (restringe volume em audiência pequena) |

### Alerta de incompatibilidade

| Situação detectada | Severidade | Mensagem recomendada |
|---|---|---|
| F1 com Cost Cap ativo | 🟡 Média | "F1 com Cost Cap pode causar underspend e dados insuficientes para decisão. Considerar mudar para Lowest Cost." |
| F1 com Bid Cap ativo | 🔴 Alta | "F1 com Bid Cap ativo: risco alto de underspend. Bid Cap em laboratório impede coleta adequada de dados." |
| F3 com Minimum ROAS target acima de 3.0x | 🟡 Média | "Minimum ROAS alto pode causar underspend na F3. Verificar se campanha está entregando ≥80% do orçamento." |
| Campanha Sales sem Lowest Cost ou Cost Cap | 🟡 Média | "Estratégia de lance não identificada. Verificar configuração." |

---

## 2. Regras de Cost Cap — Quando Recomendar

### Recomendar Cost Cap quando:
1. CPA está **volátil** (variação > ±30% entre dias) mas **dentro do range aceitável** (R$98–R$163)
2. Campanha F2/F3 com histórico de pelo menos **14 dias** de dados
3. Média de CPA está estável próxima do LIMITE (R$130) — Cost Cap evita picos acima do CORTE
4. Campanha com escala alta (R$1.000+/dia) onde cada dia fora do range custa caro

### Configuração de Cost Cap recomendada por meta:

| Meta | Cost Cap sugerido | Lógica |
|------|-------------------|--------|
| CPA ALVO (2.0x) | R$ 98–108 | Restritivo — só vai funcionar com criativos muito bons |
| CPA BOM (1.8x) | R$ 108–130 | Balanceado — entrega razoável + controle de CPA |
| CPA LIMITE (1.5x) | R$ 130–150 | Conservador — aceita qualquer criativo dentro do limite |

### ⚠️ Armadilha do Cost Cap muito baixo
Cost Cap menor que o CPA real histórico causa **underspend** (campanha não consegue gastar o orçamento porque não encontra conversões no preço definido). Sinal: campanha F2/F3 gastando < 60% do orçamento definido.

---

## 3. Regras de Bid Cap — Alertas de Restrição

### Quando alertar sobre Bid Cap restritivo

| Condição | Alerta | Ação sugerida |
|----------|--------|---------------|
| Campanha gastando < 80% do orçamento em 3+ dias | 🔴 Alta | "Possível Bid Cap muito restritivo ou Cost Cap abaixo do CPA real. Verificar entrega e considerar relaxar o cap." |
| Campanha gastando < 60% do orçamento | 🔴 Crítico | "Underspend severo. Campanha não consegue encontrar conversões no preço definido. Aumentar cap ou trocar para Lowest Cost." |
| CPM subindo + entrega caindo | 🟡 Média | "Leilão mais competitivo. Bid/Cost Cap pode estar insuficiente para competir. Monitorar." |

### Como detectar underspend nos dados
- `Gasto real < 80% × (orçamento_diário × dias_período)` = underspend
- Calcular usando `diario_*.csv` — coluna `Gasto` vs orçamento configurado (se disponível)

---

## 4. Janelas de Atribuição — Referência Rápida

> **Janela padrão desta conta:** 7-day click
> **Janela depreciada em Jan/2026:** 7-day view (não mais disponível)

### Tabela de janelas disponíveis (2026)

| Janela | O que conta | Impacto no ROAS | Quando usar |
|--------|-------------|-----------------|-------------|
| `1-day click` | Compras em até 1 dia após o clique | Mais baixo | Comparações conservadoras; produtos de decisão rápida |
| `7-day click` ← **padrão** | Compras em até 7 dias após o clique | Mais alto | Padrão da conta — produtos com ciclo de 2-7 dias |
| `1-day view` | Compras em até 1 dia após VER o anúncio (sem clicar) | Acrescenta view-through | Campanhas de awareness com conversão posterior |
| `1-day engaged view` | Compras em até 1 dia após engajar com Reels/vídeo | Acrescenta engajamento | Campanhas de vídeo com objetivo de conversão |

### Regra de interpretação: mesmo ROAS, janelas diferentes

```
Campanha A — ROAS 3.5x (7-day click)
Campanha B — ROAS 3.5x (1-day click)

Campanha B é MUITO melhor — converte imediatamente após o clique.
Campanha A pode estar atribuindo compras de remarketing ao tráfego frio.
```

### Ajuste de threshold de ROAS por janela

| Janela | ROAS mínimo aceitável | ROAS saudável | Notas |
|--------|----------------------|---------------|-------|
| 7-day click (padrão) | ≥ 2.0x | ≥ 2.5x | Referência padrão do analyst-rules.md |
| 1-day click | ≥ 1.5x | ≥ 2.0x | Janela mais curta = ROAS menor esperado |
| 1-day view | +0.3–0.5x sobre 7-day click | — | View-through infla ROAS — usar com cautela |

---

## 5. Contexto de Atribuição — Divergência Pixel vs Fonte Real

### Por que os números divergem

| Fonte | O que reporta | Limitações |
|-------|---------------|-----------|
| **Meta Pixel** (ads_*.csv) | Conversões detectadas no browser | iOS 14+ (ATT) bloqueia ~40% das conversões em usuários Apple; ad blockers; cross-device não rastreado |
| **Conversions API (CAPI)** | Conversões server-side | Mais preciso que Pixel isolado; requer implementação técnica |
| **vendas_*.csv** (Hotmart) | Faturamento real da plataforma de pagamento | **Fonte de verdade** — não depende de pixel ou browser |

**Divergência típica:** Pixel Meta reporta **60–80%** das vendas reais presentes no `vendas_*.csv`.

### Regra: quando a divergência é anormal

| Divergência (Pixel vs vendas_*.csv) | Status | Ação |
|--------------------------------------|--------|------|
| Pixel reporta 60–80% do real | ✅ Normal | iOS 14+, cross-device, ciclo >1 dia |
| Pixel reporta < 50% do real | 🟡 Verificar | Pixel pode estar mal configurado ou CAPI desativado |
| Pixel reporta > 90% do real | 🟡 Verificar | Possível dupla contagem (Pixel + CAPI sem deduplicação) |
| Pixel reporta > 100% do real | 🔴 Erro | Dupla contagem confirmada — checar deduplicação Pixel/CAPI |

---

## 6. Glossário de Métricas — Contexto de Interpretação

| Métrica | Fórmula | Interpretação nesta conta | Threshold alerta |
|---------|---------|--------------------------|-----------------|
| **CPM** | Gasto ÷ Impressões × 1000 | Custo por mil exibições. Sobe quando audiência fica saturada ou leilão mais competitivo. | CPM > R$35 = alerta de saturação |
| **CTR** | Cliques ÷ Impressões × 100 | Atratividade do criativo. CTR baixo = hook fraco ou audiência errada. | CTR < 0.90% = alerta (benchmark histórico ≥0.90%) |
| **CPC** | Gasto ÷ Cliques | Custo por clique. Elevado com CTR baixo ou CPM alto. | CPC > R$3,50 = monitorar |
| **CPA** | Gasto ÷ Compras (pixel) | Custo por aquisição via Pixel — subestima conversões reais em ~20-40%. Usar para ranking relativo de criativos. | Tabela analyst-rules.md Seção 1 |
| **CPA real** | Gasto ÷ Vendas (vendas_*.csv) | CPA com fonte de verdade. Usar para P&L e decisões estratégicas. | Mesmos thresholds da Seção 1 |
| **ROAS** | Faturamento ÷ Gasto | ROAS real usa faturamento de vendas_*.csv. ROAS estimado usa ticket médio × compras pixel. | ≥ 2.0x mínimo (janela 7-day click) |
| **VPV / VPG** | Visualizações de página de vendas | Indicador de qualidade do tráfego. Alta VPV com baixa conversão = problema na página de vendas ou oferta. | VPV/Clique < 60% = alerta de tráfego perdido |
| **IC** | Início de Checkout | Intenção de compra. Taxa IC/VPV mede atração da oferta. | IC/VPV < 15% = revisar oferta |
| **Conv. Checkout** | Vendas ÷ IC × 100 | Taxa de fechamento. | ≥ 11% LVC VSL B; ≥ 15% MDA VSL A; ≥ 21% MDA VSL C |
| **Frequência** | Impressões ÷ Alcance | Quantas vezes a mesma pessoa viu o anúncio. | > 3.0x F2; > 2.5x F3 = alerta fadiga |

---

## 7. Checklist de Atribuição — Antes de Publicar Análise

Antes de apresentar qualquer análise com dados de performance, verificar:

- [ ] **Janela definida:** Qual janela de atribuição foi usada nos dados da Meta API? Declarar no relatório.
- [ ] **Fonte dos números:** Faturamento veio de `vendas_*.csv` ou de dados do Pixel? Indicar claramente.
- [ ] **Divergência mapeada:** Se usou Pixel para CPA, lembrar que subestima ~20-40% as conversões reais.
- [ ] **Comparação válida:** Se comparando dois períodos, a janela de atribuição é a mesma em ambos?
- [ ] **7-day view:** Não usar janela 7-day view em dados de 2026 (depreciada em 12/01/2026).
- [ ] **ROAS calculado corretamente:** Dividir faturamento real (vendas_*.csv) pelo gasto real (diario_*.csv) — não pelo estimado.

---

## 8. Seção "Contexto de Atribuição" para Relatórios

Incluir este bloco em todo relatório quando a fonte de dados incluir métricas do Pixel Meta:

```markdown
### Contexto de Atribuição

- **Janela:** 7-day click (padrão da conta)
- **Fonte de faturamento:** vendas_*.csv (Hotmart) — fonte de verdade
- **Fonte de CPA por criativo:** ads_*.csv — dados do Pixel Meta (subestima ~20-40% das vendas reais)
- **Nota iOS 14+:** Conversões de usuários Apple podem não estar sendo rastreadas pelo Pixel.
  Divergência entre Pixel e faturamento real é esperada e normal.
- **7-day view:** Depreciada em Jan/2026 — não disponível nos dados atuais.
```

---

## 9. Referência Rápida — O que fazer quando CPA está fora do target

| Situação | Diagnóstico | Ação |
|----------|-------------|------|
| CPA alto + CTR baixo | Hook fraco — criativos não atraem clique | Renovar criativos na F1 |
| CPA alto + CTR bom + VPV baixo | Tráfego perdendo interesse antes da página | Revisar copy do anúncio ou URL de destino |
| CPA alto + VPV bom + IC baixo | Oferta não converte — problema na landing page | Revisar página/VSL |
| CPA alto + IC bom + Conv. Checkout baixo | Checkout com fricção ou preço | Revisar checkout, preço, urgência |
| CPA alto + tudo normal | Audiência saturada ou leilão mais caro | Verificar frequência + expandir audiência |
| CPA alto + campanha nova (< 3 dias) | Learning Phase — aguardar | Não tomar decisão antes de 3 dias |

---

## 10. Fontes

- `docs/meta-knowledge/meta-05-bidding-attribution.md` — documentação base completa
- `config/analyst-rules.md` — Seções 1 (CPA targets), 12 (ASC), 14 (attribution window)
- `config/account-benchmarks.md` — benchmarks históricos fev/2026

---
*bidding-attribution-guide.md | Meta Ads Intelligence | 2026-03-28*
