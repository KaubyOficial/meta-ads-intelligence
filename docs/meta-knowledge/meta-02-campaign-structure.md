# Meta Ads — Estrutura de Campanhas e Objetivos

> **Fonte:** Meta Business Help Center + Meta Ads Manager Documentation
> **Referência:** 2025-2026
> **Uso:** Base de conhecimento para análise de estrutura de campanhas no meta-ads-intelligence

---

## 1. Hierarquia de Campanhas

O Meta Ads Manager organiza todos os anúncios em uma estrutura hierárquica de três níveis: Campanha → Conjunto de Anúncios → Anúncio. Cada nível tem responsabilidades distintas e impacta como os algoritmos da Meta otimizam a entrega.

```
Campanha (Campaign)
│   └─ Objetivo de marketing (ODAX)
│   └─ Orçamento (Advantage Campaign Budget / CBO)
│   └─ Special Ad Category
│   └─ A/B Testing
│
├── Conjunto de Anúncios (Ad Set)
│   └─ Público-alvo (Core, Custom, Lookalike, Advantage+)
│   └─ Posicionamentos (Placements)
│   └─ Orçamento (ABO, quando CBO não está ativo)
│   └─ Programação (schedule / dayparting)
│   └─ Meta de otimização (Optimization Goal)
│   └─ Estratégia de lance (Bid Strategy)
│   └─ Janela de atribuição (Attribution Window)
│
└── Anúncio (Ad)
    └─ Formato criativo (imagem, vídeo, carrossel, collection, etc.)
    └─ Texto principal, headline, descrição, CTA
    └─ URL de destino
    └─ Parâmetros UTM e tracking
    └─ Pixel / Conversions API events
```

---

### 1.1 Nível Campanha (Campaign)

O nível de campanha é o topo da hierarquia e define o **objetivo estratégico** da iniciativa publicitária. É aqui onde se responde: "O que quero que as pessoas façam ao ver meu anúncio?"

**Decisões tomadas no nível de campanha:**
- **Objetivo de campanha** (um dos 6 objetivos ODAX — detalhados na seção 2)
- **Orçamento global** via Advantage Campaign Budget / CBO (opcional, mas recomendado para escala)
- **Categorias de anúncios especiais** (Credit, Employment, Housing, Politics, Financial Services)
- **Estratégia de lance global** quando o Advantage Campaign Budget está ativo
- **A/B Testing nativo** (Experimentos com divisão de audiência sem sobreposição)

**Impacto no algoritmo:** O objetivo selecionado instrui o algoritmo a entregar os anúncios para pessoas com maior probabilidade de realizar a ação desejada. Escolher o objetivo errado significa otimização para o público errado, desperdiçando orçamento.

**Princípio-chave:** Uma campanha = um objetivo. Misturar objetivos dentro de uma campanha impede a otimização eficiente.

**Boas práticas 2025:**
- Menos campanhas com mais orçamento concentrado performam melhor do que muitas campanhas fragmentadas
- O algoritmo precisa de pelo menos **50 conversões por conjunto de anúncios por semana** para otimizar efetivamente
- Nomear campanhas com convenção clara: `[Objetivo] - [Produto/Oferta] - [Audiência] - [Data]`

---

### 1.2 Nível Conjunto de Anúncios (Ad Set)

O conjunto de anúncios é o nível intermediário onde se define **para quem** e **onde** os anúncios serão exibidos. É também onde se configura o orçamento individual (quando não se usa CBO) e os parâmetros de entrega.

**Configurações disponíveis:**

| Configuração | Opções principais |
|---|---|
| Audiência | Core Audiences, Custom Audiences, Lookalike Audiences, Advantage+ Audience |
| Posicionamentos | Automático (Advantage+ Placements) ou Manual (19 posicionamentos) |
| Orçamento (ABO) | Diário ou Vitalício |
| Programação | Sempre ativo, datas específicas, dayparting (com orçamento vitalício) |
| Meta de otimização | Conversões, Cliques, Impressões, Alcance, ThruPlay, Leads, etc. |
| Estratégia de lance | Menor custo, Cap de custo, Cap de lance, ROAS mínimo |
| Janela de atribuição | 1-dia clique, 7-dias clique, 1-dia visualização, combinações |
| Local de conversão | Website, App, Messenger, WhatsApp, Instagram, Chamadas, Loja física |

**Meta de otimização por objetivo:** Dentro do objetivo da campanha, o Ad Set permite escolher uma sub-meta. Exemplo: campanha com objetivo "Sales" pode otimizar para Compras, Adições ao Carrinho, Visualizações de Landing Page, etc.

**Advantage+ Placements (recomendado):** Permite que a Meta distribua os anúncios automaticamente nos posicionamentos com melhor desempenho. Reduz CPM e aumenta escala disponível.

**Boas práticas 2025:**
- Usar Advantage+ Placements para maximizar alcance eficiente
- Evitar excesso de ad sets por campanha — fragmenta o orçamento e dificulta o aprendizado
- Consolidar audiências similares em um único ad set sempre que possível
- Cada ad set deve atingir pelo menos 50 eventos de otimização/semana para sair da fase de aprendizado

---

### 1.3 Nível Anúncio (Ad)

O anúncio é o nível mais granular — é o que o usuário final efetivamente vê. Cada ad set pode conter múltiplos anúncios com diferentes criativos.

**Elementos configuráveis:**

- **Formato criativo:** Imagem única, Vídeo, Carrossel, Collection, Instant Experience, Stories/Reels
- **Texto primário (Primary Text):** Corpo do anúncio (até 125 caracteres recomendados; até 500 suportados)
- **Headline:** Título (até 27 caracteres recomendados)
- **Descrição:** Texto adicional abaixo do headline
- **Call to Action (CTA):** "Comprar Agora", "Saiba Mais", "Cadastre-se", "Enviar Mensagem", etc.
- **URL de destino:** Link para onde o usuário será direcionado após o clique
- **Parâmetros UTM:** Para rastreamento em ferramentas de analytics externas
- **Pixel Events:** Associação com eventos de conversão do Meta Pixel / CAPI

**Dynamic Creative (Criativo Dinâmico):** Permite carregar múltiplas versões de cada elemento (até 5 imagens, 5 textos, 5 headlines) e o algoritmo testa e otimiza automaticamente as combinações de maior performance.

**Advantage+ Creative:** Automação avançada que pode ajustar brilho, contraste, adicionar música, aplicar filtros e outros elementos para otimizar a performance criativa automaticamente.

---

## 2. Os 6 Objetivos de Campanha (ODAX)

O sistema **ODAX (Outcome-Driven Ad Experiences)** foi introduzido pela Meta para consolidar os objetivos de campanha anteriores em 6 categorias alinhadas a resultados de negócio. Essa estrutura também permite que o algoritmo otimize com base em sinais de desempenho mais precisos.

> **Importante:** O objetivo escolhido define quais formatos, posicionamentos, metas de otimização e recursos de automação ficam disponíveis. É a decisão mais impactante da estrutura de campanha.

---

### 2.1 Awareness (Reconhecimento)

**O que faz:** Maximiza o número de pessoas que veem o anúncio e constroem memória sobre a marca. A Meta otimiza para **impressões de qualidade** e **alcance único**.

**Quando usar:**
- Lançamento de nova marca, produto ou serviço
- Campanhas sazonais ou de branding de longo prazo
- Aumentar Share of Mind antes de uma campanha de conversão
- Nichos com baixo reconhecimento de marca (audiência fria sem nenhum contato anterior)

**Metas de otimização disponíveis:**
- Maximizar alcance (Reach)
- Maximizar impressões
- Ad Recall Lift (estimativa de recall da marca)
- ThruPlay (usuários que assistiram pelo menos 15 segundos do vídeo ou até o fim)
- Video Views (2 segundos contínuos)

**Métricas relevantes:** CPM, Alcance, Frequência, Ad Recall Lift, ThruPlay Rate

**Formatos recomendados:** Vídeo (especialmente Reels e Stories), Imagem

**Limitação crítica:** Awareness não otimiza para cliques ou conversões. É ferramenta de topo de funil — não esperar leads ou vendas diretas desse objetivo.

---

### 2.2 Traffic (Tráfego)

**O que faz:** Direciona pessoas para um destino específico: site, aplicativo, página do Facebook, ou conversa no Messenger/WhatsApp. A Meta otimiza para usuários com maior probabilidade de clicar.

**Quando usar:**
- Atrair visitantes para o site ou landing page
- Gerar tráfego para artigos, conteúdos de blog, páginas de produto
- Aquecer audiências para retargeting posterior
- Campanhas de topo/meio de funil com foco em visitas qualificadas

**Metas de otimização disponíveis:**
- Link Clicks — maximiza cliques brutos no link
- Landing Page Views — otimiza para usuários que aguardam a página carregar (maior qualidade; requer Pixel)
- Daily Unique Reach — limita impressões por pessoa
- Impressions — exposição bruta

**Métricas relevantes:** CPC, CTR, CPL (custo por Landing Page View), Taxa de rejeição

**Formatos recomendados:** Imagem, Vídeo, Carrossel

**Atenção:** "Link Clicks" conta qualquer clique incluindo usuários que abandonam imediatamente; "Landing Page Views" exige que o Pixel dispare na página — é mais preciso e recomendado quando o Pixel está instalado corretamente.

---

### 2.3 Engagement (Engajamento)

**O que faz:** Aumenta interações com conteúdo — curtidas, comentários, compartilhamentos, mensagens iniciadas, ou visualizações de vídeo. A Meta otimiza para usuários com comportamento de engajamento.

**Quando usar:**
- Aumentar prova social em publicações (likes, comentários)
- Impulsionar eventos do Facebook
- Gerar conversas via Messenger, WhatsApp ou Instagram Direct (vendas via chat)
- Construir audiências de engajamento para retargeting posterior
- Criar comunidade em torno da marca

**Metas de otimização disponíveis:**
- Post Engagement (curtidas, comentários, compartilhamentos)
- Page Likes
- Event Responses (respostas a eventos)
- Conversations (Messenger, WhatsApp, Instagram Direct)
- ThruPlay / Video Views

**Métricas relevantes:** CPE (Custo por Engajamento), Taxa de engajamento, Custo por mensagem iniciada

**Formatos recomendados:** Imagem, Vídeo, Carrossel (exceto para objetivos de mensagens)

**Nota 2025:** O objetivo Engagement inclui otimização para Mensagens, tornando-o útil para negócios que vendem via chat — especialmente relevante no mercado brasileiro.

---

### 2.4 Leads

**O que faz:** Coleta informações de contato de potenciais clientes. Pode ser via formulário nativo do Meta (Instant Forms — sem sair da plataforma) ou redirecionando para landing page externa.

**Quando usar:**
- Geração de leads para funis de vendas
- Captação de e-mails para listas de nutrição
- Agendamento de consultas, demos, visitas
- Cadastros para webinars, listas de espera, conteúdos premium
- Segmentos B2B onde a venda requer contato humano posterior

**Metas de otimização e métodos de captação disponíveis:**

| Método | Descrição |
|---|---|
| Instant Forms | Formulário nativo Meta (pré-preenchido com dados do perfil). Sem sair do app. Alto volume, qualidade variável. |
| Website | Redireciona para landing page externa (requer Pixel com evento Lead). Maior intenção, menor volume. |
| Messenger / WhatsApp / Instagram DM | Abre fluxo de conversa qualificatória via chat. |
| Calls | Direciona chamadas telefônicas direto do anúncio. |

**Instant Forms — tipos:**
- **More Volume:** Formulário simples, poucos campos, pré-preenchido. Maior volume, qualidade mais baixa.
- **Higher Intent:** Adiciona tela de revisão antes do envio. Reduz volume mas aumenta qualidade do lead.

**Otimizações disponíveis:**
- Leads (qualquer evento de lead)
- Conversion Leads (otimiza para leads que viram clientes — requer integração CRM via CAPI)
- Quality Leads (requer feedback de qualidade de lead configurado)

**Métricas relevantes:** CPL (Custo por Lead), Taxa de conversão de formulário, Taxa de qualificação

**Boas práticas:** Integrar Instant Forms com CRM via API de Conversões da Meta para nutrição imediata e para treinar o algoritmo com dados de lead qualificado.

---

### 2.5 App Promotion

**O que faz:** Gera instalações de aplicativos móveis e/ou reengajamento de usuários existentes. Exclusivo para anunciantes com apps registrados no Meta.

**Quando usar:**
- Lançamento de novo app
- Escalar instalações com CAC (Custo de Aquisição por Cliente) controlado
- Reengajar usuários que instalaram mas estão inativos
- Incentivar ações específicas dentro do app (compras in-app, cadastros, uso de features)

**Metas de otimização disponíveis:**
- App Installs — maximizar downloads
- App Events — otimizar para eventos in-app específicos (requer SDK Meta integrado)
- Value — otimizar para maior valor de compras in-app
- ROAS Mínimo para compras in-app
- Link Clicks para App Store

**Considerações iOS (ATT):** Após o iOS 14.5, usuários que não consentiram via App Tracking Transparency (ATT) da Apple têm rastreamento limitado. Campanhas iOS exigem configuração via SKAdNetwork (SKAN) para atribuição correta.

**Métricas relevantes:** CPI (Custo por Instalação), ROAS in-app, Retention Rate, LTV (Lifetime Value)

**Formatos recomendados:** Vídeo (demonstrações do app), Imagem

---

### 2.6 Sales (Vendas)

**O que faz:** Otimiza para as pessoas com maior probabilidade de comprar. É o objetivo de fundo de funil por excelência — usa todos os sinais comportamentais históricos do Pixel e do CAPI para encontrar compradores.

**Quando usar:**
- Campanhas de conversão com foco em compras (e-commerce, infoprodutos)
- Retargeting de visitantes do site, abandonadores de carrinho
- Audiências de clientes ativos para upsell/cross-sell
- Campanhas com catálogo de produtos (Dynamic Ads)
- Qualquer campanha de direct-response com evento de conversão mensurável

**Locais de conversão disponíveis:**
- **Website** — requer Meta Pixel com evento de conversão configurado (Purchase, Lead, etc.)
- **App** — requer Facebook SDK integrado
- **Messenger / WhatsApp / Instagram** — conversas que convertem
- **Calls** — conversões via chamada telefônica
- **Store** — tráfego para loja física (Offline Conversions)

**Metas de otimização disponíveis:**
- Conversions — otimizar para evento específico do Pixel (ex: Purchase)
- Value — otimizar para maior valor total de compras (não apenas volume)
- Product Catalog Sales — retargeting dinâmico com feed de produtos (Dynamic Ads)
- Link Clicks, Landing Page Views (tráfego qualificado, não recomendado para otimização direta de conversão)

**Advantage+ Shopping Campaigns (ASC):** Formato automatizado para e-commerce. Une prospecção e retargeting em uma única campanha gerenciada por IA. Testa até 150 combinações criativas automaticamente. Meta reporta média de **17% menor CPP** vs. campanhas manuais.

**Métricas relevantes:** ROAS, CPP (Custo por Compra), Taxa de conversão, AOV (Valor Médio do Pedido)

**Requisito técnico crítico:** Pixel instalado corretamente com eventos de conversão configurados. Implementar também a API de Conversões (CAPI) para recuperar eventos bloqueados por ad blockers e restrições iOS.

---

## 3. Orçamento: CBO vs Orçamento por Ad Set

### 3.1 Campaign Budget Optimization (CBO) — Advantage Campaign Budget

O CBO, renomeado para **Advantage Campaign Budget** no Meta Ads Manager, é um sistema onde se define **um único orçamento no nível da campanha** e o algoritmo distribui automaticamente esse orçamento entre os ad sets com base na performance em tempo real.

**Como funciona:**
- O orçamento é um "pool" compartilhado entre todos os ad sets da campanha
- A Meta monitora continuamente o desempenho de cada ad set
- Maior verba é alocada automaticamente para ad sets com melhor resultado (CPR — Custo por Resultado)
- Ad sets com performance fraca recebem menos orçamento, mas não são zerados automaticamente
- É possível configurar **limites mínimos e máximos de gasto por ad set** para manter controle parcial

**Vantagens do CBO:**
- Maximiza eficiência do orçamento total sem intervenção manual constante
- Meta reporta até **17% de aumento no ROAS** e **27% de redução de custos** em campanhas multi-audiência
- Usuários CBO registram até **12% menor CPP** (Custo por Compra) em média
- Escalar é mais simples: aumentar um único número de orçamento
- Sem reset de aprendizado ao aumentar o budget da campanha (ao contrário do ABO)

**Desvantagens do CBO:**
- Perda de controle granular — sem garantia de gasto por ad set específico
- Ad sets com audiências menores podem ser "sufocados" pelo algoritmo
- Não ideal para testes isolados de audiências (ad sets recebem orçamento desigual)
- Algoritmo pode concentrar gasto em um único ad set, ignorando outros completamente

**Configurações de controle dentro do CBO:**
- **Orçamento diário vs. vitalício:** Diário é mais estável; Vitalício permite pacing otimizado em janelas definidas e habilita dayparting
- **Spend Limits por Ad Set:** Mínimo (floor) e/ou máximo (cap) de gasto por ad set mesmo com CBO ativo — mas limita a capacidade de otimização do algoritmo

---

### 3.2 Orçamento por Ad Set (ABO — Ad Set Budget)

No ABO, cada ad set tem seu **próprio orçamento independente**. O algoritmo otimiza dentro dos limites de cada conjunto, sem redistribuição entre eles.

**Vantagens do ABO:**
- Controle preciso: garantia de quanto cada ad set gasta
- Ideal para testes — cada ad set recebe orçamento igual, permitindo comparação justa
- Útil quando há ad sets com audiências muito diferentes em tamanho
- Testa novas audiências com budget controlado sem risco de diluir campanhas principais

**Desvantagens do ABO:**
- Requer mais gerenciamento manual e monitoramento constante
- Pode resultar em desperdício se ad sets fracos continuam gastando sem intervenção
- Escalar requer ajustes manuais por ad set
- Qualquer mudança significativa de budget reinicia a fase de aprendizado do ad set

---

### 3.3 Quando usar cada um

| Situação | Recomendação |
|---|---|
| Fase de teste de audiências | **ABO** — controle igual por ad set, dados comparáveis |
| Teste de criativos isolados | **ABO** — garantia de gasto igual por criativo |
| Campanha já otimizada, pronta para escalar | **CBO** — algoritmo aloca para onde performa melhor |
| Múltiplos ad sets com audiências similares | **CBO** — evita sobreposição, maximiza entrega |
| Ad sets com tamanhos de audiência muito diferentes | **ABO** — evita que o maior "sufoque" o menor |
| Advantage+ Shopping Campaigns (ASC) | **CBO obrigatório** — estrutura nativa do formato |
| Budget diário acima de 5x o CPA alvo | **CBO** — algoritmo tem dados suficientes para otimizar |
| Conta nova sem histórico de conversões | **ABO** — maior controle durante a fase de aprendizado inicial |

**Estratégia híbrida recomendada (2025):**
1. **Fase de Teste:** ABO com orçamento igual por ad set para identificar audiências e criativos vencedores
2. **Fase de Escala:** Migrar vencedores para nova campanha com CBO para maximizar resultados

**Orçamento mínimo para CBO funcionar bem:**
- Budget semanal deve ser pelo menos **50x o CPA alvo**
- Exemplo: CPA alvo R$100 → Budget mínimo semanal R$5.000 → ~R$715/dia
- Abaixo desse patamar, o algoritmo não tem dados suficientes para otimizar de forma confiável

---

## 4. O Leilão de Anúncios Meta

### 4.1 Como funciona o leilão

O Meta Ads utiliza um sistema de **leilão em tempo real** (Real-Time Bidding). A cada vez que um usuário abre o Feed, Stories, Reels ou qualquer superfície com anúncios, a Meta realiza um leilão instantâneo entre todos os anúncios elegíveis para aquele usuário específico naquele contexto.

**Características do leilão:**
- Ocorre em milissegundos, bilhões de vezes por dia
- É um leilão de **segundo preço** (Vickrey-style): o vencedor paga apenas o suficiente para superar o segundo maior lance, não o seu lance máximo
- **Quem paga mais não necessariamente vence** — qualidade e relevância são fatores críticos
- Cada usuário vê apenas o anúncio vencedor (ou nenhum anúncio, se nenhum passar o limiar de qualidade mínimo)
- Não existe "garantia" de que um anúncio será exibido — sempre há competição

---

### 4.2 Fórmula do Valor Total

O vencedor do leilão é determinado pelo maior **Valor Total (Total Value)**:

```
Valor Total = Lance do Anunciante × Taxa de Ação Estimada + Pontuação de Qualidade
```

Em inglês (terminologia oficial Meta):

```
Total Value = Advertiser Bid × Estimated Action Rate (EAR) + Ad Quality Score
```

**Interpretação prática:**
- Um anúncio com **lance alto mas qualidade baixa** pode perder para um com **lance menor mas qualidade excelente**
- Melhorar a qualidade criativa tem impacto direto no custo — anúncios melhores pagam menos pelo mesmo resultado
- Os três componentes são multiplicativos e aditivos: fraqueza em qualquer um penaliza o resultado final

---

### 4.3 Quality Score e Relevância

O Meta Ads Manager expõe três diagnósticos de qualidade para cada anúncio (visíveis na coluna de diagnóstico):

| Diagnóstico | O que mede | Comparação |
|---|---|---|
| **Quality Ranking** | Qualidade percebida do criativo vs. concorrentes | Outros anúncios competindo pela mesma audiência |
| **Engagement Rate Ranking** | Taxa de engajamento esperada vs. concorrentes | Outros anúncios competindo pela mesma audiência |
| **Conversion Rate Ranking** | Taxa de conversão esperada vs. concorrentes | Outros anúncios com o mesmo objetivo e audiência |

**Escalas de diagnóstico:**
- Above Average (top 55%)
- Average (35%–55%)
- Below Average (bottom 35%)
- Below Average (bottom 20%)

**Sinais que compõem o Ad Quality Score:**
- **Feedback positivo:** curtidas, comentários, compartilhamentos, saves, cliques
- **Feedback negativo:** "Ocultar anúncio", "Não quero ver isso", denúncias, bloqueios
- **Relevância do criativo** para a audiência-alvo com base no conteúdo
- **Qualidade da experiência pós-clique:** Se o usuário clica mas rejeita a página imediatamente (bounce rápido), o anúncio é penalizado
- **Práticas proibidas:** Clickbait, antes/depois de saúde, conteúdo sensacionalista — penalizam automaticamente a qualidade

---

### 4.4 Como melhorar desempenho no leilão

**Melhorar a Taxa de Ação Estimada (EAR):**
- Instalar e verificar o Meta Pixel em todas as páginas relevantes
- Implementar API de Conversões (CAPI) para recuperar eventos perdidos por bloqueio de cookies e restrições iOS
- Usar audiences personalizadas de alta qualidade (clientes existentes, visitantes do site com intenção)
- Consolidar ad sets para concentrar sinais de conversão e sair da Fase de Aprendizado
- Acumular histórico de conversões (mínimo 50/semana por ad set)

**Melhorar a Qualidade do Anúncio:**
- Criar criativos altamente relevantes para a audiência-alvo
- Testar múltiplos criativos por ad set (3-5 variações) para identificar vencedores
- Monitorar feedback negativo e pausar anúncios com alta taxa de "ocultar"
- Garantir alinhamento entre o criativo e a landing page (consistência da mensagem)
- Renovar criativos regularmente para evitar fadiga criativa (queda de CTR = queda de qualidade)

**Estratégia de lance:**
- Com pouco histórico de dados: usar **Lowest Cost** para maximizar volume de resultados
- Com CPA alvo definido e dados suficientes: usar **Cost Cap**
- Para controle máximo por leilão: usar **Bid Cap**
- Para campanhas de e-commerce com foco em margem: usar **Minimum ROAS**

**Value Rules (lançadas em junho 2025):**
Permitem multiplicadores de lance para segmentos de audiência específicos (ex: +200% de lance para mulheres de 25-34 no iOS). Disponíveis para campanhas de Sales com otimização por valor.

**Fase de Aprendizado:**
- Todo novo ad set entra em Fase de Aprendizado — o algoritmo está calibrando
- Meta recomenda **não fazer mudanças significativas** durante esse período
- A fase termina após ~50 eventos de otimização (geralmente 7-14 dias)
- "Aprendizado Limitado" (Learning Limited) indica dados insuficientes — soluções: expandir audiência, usar evento de otimização de funil mais alto (ex: trocar Purchase por Add to Cart), ou aumentar orçamento

---

## 5. Configurações de Campanha

### 5.1 Special Ad Categories

A Meta exige que determinadas categorias de negócio sejam declaradas ao criar campanhas. Isso é parte das políticas da plataforma contra discriminação em áreas protegidas por lei.

**Categorias disponíveis:**

| Categoria | Exemplos de produtos/serviços |
|---|---|
| **Credit** | Cartões de crédito, empréstimos, financiamentos, hipotecas |
| **Employment** | Vagas de emprego, agências de recrutamento, plataformas de trabalho |
| **Housing** | Compra/venda/aluguel de imóveis, seguros residenciais |
| **Social Issues, Elections or Politics** | Questões políticas, candidaturas, causas sociais |
| **Financial Products and Services** | Produtos financeiros em geral — **obrigatório desde início de 2025** para qualquer produto financeiro |

**Restrições impostas ao declarar uma Special Ad Category:**

| Restrição | Detalhe |
|---|---|
| Faixa etária | Deve incluir 18–65+. Sem exclusão de faixas etárias. |
| Gênero | Todos os gêneros devem ser incluídos. |
| Localização | Targeting por estado/país permitido, mas **ZIP code/CEP não é permitido**. |
| Exclusão geográfica | **Não permitida**. |
| Interesses e comportamentos | Limitados ou indisponíveis. |
| Lookalike Audiences | Disponíveis com restrições (sem targeting demográfico sensível). |
| Advantage+ Targeting | **Não disponível**. |

**Certificação (março 2025 em diante — EUA):** Anunciantes usando listas de clientes para Housing, Employment ou Financial Products devem certificar que as listas não contêm informações sensíveis do consumidor. Opção aparece no Ads Manager durante a criação.

**Consequências de não declarar:** Anúncios rejeitados, campanha pausada, possível suspensão da conta em casos reincidentes.

---

### 5.2 A/B Testing nativo

O Meta Ads Manager oferece uma ferramenta nativa de A/B Testing (chamada de "Experimentos") para comparar variáveis de forma estatisticamente válida.

**Como funciona:**
- A Meta divide aleatoriamente a audiência em grupos **sem sobreposição** (cada usuário vê apenas uma variação)
- O orçamento é dividido igualmente entre as variações
- A Meta calcula a significância estatística e declara um vencedor ao final
- Pode comparar: audiências, posicionamentos, criativos, estratégias de lance, objetivos

**Tipos de testes suportados:**
- Criativo vs. Criativo (imagem, vídeo, copy, headline)
- Audiência vs. Audiência (qual segmentação converte melhor)
- CBO vs. ABO (comparar estratégias de orçamento)
- Objetivo vs. Objetivo (comparar diferentes objetivos de campanha)
- Advantage+ Audience vs. audiência manual
- Posicionamentos automáticos vs. manuais

**Creative Testing Nativo (2025 — novidade):**
Recurso que permite testar até **5 criativos dentro de um único ad set**, sem fragmentar o orçamento. O algoritmo distribui igualmente no início e, após identificar o vencedor, redireciona o orçamento automaticamente.

**Boas práticas de A/B Testing:**
- Testar apenas **uma variável por vez** para resultados conclusivos
- Definir a métrica de sucesso (KPI primário) antes de iniciar
- Aguardar significância estatística (geralmente 7-14 dias, mínimo ~100 eventos de otimização por variação)
- Budget mínimo: suficiente para gerar 50-100 eventos de otimização por variação
- Documentar resultados e construir base de conhecimento criativo ao longo do tempo

---

### 5.3 Advantage Campaign Budget

Parte da suite **Advantage+** da Meta — conjunto de ferramentas de automação baseadas em IA lançadas para simplificar e otimizar campanhas:

**Suite Advantage+ completa:**

| Produto | O que automatiza |
|---|---|
| **Advantage Campaign Budget** | Distribuição de orçamento entre ad sets (antigo CBO) |
| **Advantage+ Audience** | Targeting — Meta escolhe a audiência ideal com base em sinais de performance |
| **Advantage+ Placements** | Posicionamentos — Meta escolhe onde exibir para melhor resultado |
| **Advantage+ Creative** | Criativos — Meta ajusta elementos visuais (brilho, contraste, música, textos) automaticamente |
| **Advantage+ Shopping Campaigns (ASC)** | Campanha completa de e-commerce gerenciada inteiramente por IA |
| **Advantage+ App Campaigns** | Campanha de apps totalmente automatizada |

**Advantage+ Shopping Campaigns (ASC) — detalhes:**
- Disponível para campanhas de Sales com objetivo de compra
- Combina audiências frias (prospecção) e quentes (retargeting) em uma única campanha
- Testa até 150 combinações criativas automaticamente
- Meta reporta média de **9% menor CPA** e até **17% menor CPP** vs. campanhas manuais
- Permite definir percentual máximo do budget dedicado a clientes existentes vs. novos clientes
- Recomendação: máximo de 1 ASC por conta por vez

**Quando usar a automação Advantage+:**
- E-commerce com catálogo de produtos e forte histórico de pixel
- Contas com dados suficientes de conversão (> 50 compras/semana)
- Quando o objetivo é escalar com mínima gestão manual
- Ao testar se automação performa melhor que configuração manual (via A/B Test)

**Quando manter controle manual:**
- Fase de teste e aprendizado (conta nova, produto novo, audiência nova)
- B2B ou negócios de serviços onde segmentação específica é crítica
- Quando compliance ou controle de posicionamento é necessário
- Quando se precisa de transparência total na alocação de orçamento

---

## 6. Formatos de Anúncio por Objetivo

| Formato | Awareness | Traffic | Engagement | Leads | App Promotion | Sales |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Imagem Única | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Vídeo Único | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Carrossel | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| Collection | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Instant Experience | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Catalog / Dynamic Ads | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Stories/Reels (9:16) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Instant Forms (Lead Ads) | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

> ✅ = Disponível | ❌ = Não disponível | ⚠️ = Disponível com limitações de sub-objetivo

**Detalhamento dos principais formatos:**

**Imagem Única:** Formato mais simples e rápido de criar. Ideal para mensagens diretas e claras.
- Proporção recomendada: 1:1 (quadrado) ou 4:5 (retrato) para Feed; 9:16 para Stories/Reels
- Resolução mínima: 1080x1080px | Formato: JPG ou PNG | Tamanho máx: 30MB

**Vídeo Único:** Maior capacidade de storytelling. Vídeos curtos (6-15s) para Awareness; 30-60s para Conversões com audiências quentes.
- Formatos: MP4, MOV, GIF | Proporções: 1:1, 4:5, 16:9, 9:16 | Tamanho máx: 4GB
- Duração: 1 segundo até 241 minutos (Feed); até 60s para maioria dos posicionamentos
- **Legendas altamente recomendadas** — 80%+ dos usuários assiste sem som

**Carrossel:** Até 10 cards, cada um com imagem/vídeo, headline e URL individuais.
- Especificação: 1080x1080px por card | 2 a 10 cards
- Aumento médio de CTR: 20-30% vs. imagem única em e-commerce

**Collection:** Imagem de capa/vídeo com grade de produtos abaixo. Ao clicar, abre Instant Experience (tela cheia) sem sair do app da Meta.
- Mobile-only | Ideal para e-commerce com catálogo
- Cover: 1200x628px (landscape) ou 1:1 (square)

**Catalog / Dynamic Ads:** Conecta ao catálogo de produtos da Meta e exibe automaticamente produtos relevantes para cada usuário com base em comportamento de navegação e compra. Essencial para retargeting de e-commerce em escala.

**Stories e Reels:** Formato vertical full-screen (9:16). Alta visibilidade e imersão.
- Especificação: 1080x1920px
- Manter conteúdo principal na zona segura central (evitar top 14% e bottom 20% da tela)
- Hook nos primeiros 1-2 segundos é crítico
- Reels: até 30 segundos (Facebook) / 60 segundos (Instagram)

---

## 7. Fontes Oficiais

- [Meta Business Help Center — Criar campanhas de anúncios no Gerenciador de Anúncios](https://www.facebook.com/business/help/621956575422138)
- [Meta for Business — A/B Testing nativo](https://www.facebook.com/business/measurement/ab-testing)
- [Bir.ch — 6 Facebook Campaign Objectives (ODAX Guide 2025)](https://bir.ch/blog/facebook-ad-objectives)
- [MagicBrief — Meta's 6 Ad Objectives: What They Are & How to Use Them](https://magicbrief.com/post/metas-6-ad-objectives---what-they-are-how-to-use-them-effectively)
- [AdAmigo — CBO vs ABO: Choosing the Right Budget Strategy](https://www.adamigo.ai/blog/cbo-vs-abo-choosing-the-right-budget-strategy)
- [AdAmigo — CBO Best Practices for Meta Ads 2025](https://www.adamigo.ai/blog/cbo-best-practices-meta-ads)
- [AdAmigo — Campaign vs. Ad Set Budgets: Key Differences](https://www.adamigo.ai/blog/campaign-vs-ad-set-budgets-key-differences)
- [Bir.ch — Advantage+ Shopping Campaigns Guide 2025](https://bir.ch/blog/advantage-plus-sales-campaigns-guide)
- [Mohit Dave — What is Total Value (Quality Score) in Facebook Ads?](https://www.mohitdave.com/facebook-ads-total-value/)
- [Bind Media — What Can We Learn From How The Meta Ads Auction Works](https://bind.media/insights/what-can-we-learn-from-how-the-meta-ads-auction-works)
- [Conv3rt — How does the Meta ads auction system work?](https://conv3rt.co.uk/articles/how-does-the-meta-ads-auction-system-work/)
- [Data Axle — The 2025 Meta special ad categories rules you need to know](https://www.data-axle.com/resources/blog/meta-special-ad-categories-rules/)
- [LeadEnforce — Meta Special Ad Category: What It Is and How to Stay Compliant](https://leadenforce.com/blog/meta-special-ad-category-what-it-is-and-how-to-stay-compliant)
- [Jon Loomer Digital — 83 Changes to Meta Advertising in 2025](https://www.jonloomer.com/meta-advertising-changes-2025/)
- [Dataslayer — Meta Ad Formats in 2025: Quick Guide](https://www.dataslayer.ai/blog/meta-ad-formats-in-2025-guide)
- [Flighted — The Best Meta Ads Account Structure in 2026](https://www.flighted.co/blog/best-meta-ads-account-structure-2026)
- [Ads Uploader — ABO vs CBO: Which Budget Strategy Actually Works in 2026](https://adsuploader.com/blog/abo-vs-cbo)
- [Pansofic — Meta Ads 2025 Guide: Setup & Campaign Strategies](https://www.pansofic.com/blog/meta-ads-2025-setup-and-campaign-guide)
- [Foxwell Digital — Sensitive Ad Categories: Meta's 2025 Rule Changes](https://www.foxwelldigital.com/blog/sensitive-ad-categories-changes-coming-to-meta-in-2025)

---

*Documento gerado em: 2026-03-28*
*Versão: 1.0*
*Próxima revisão recomendada: 2026-09-01*
