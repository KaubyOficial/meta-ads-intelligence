# Meta Ads — Segmentação de Audiência

> **Fonte:** Meta Business Help Center, Jon Loomer Digital, WordStream, AdNabu, CropInk, Lebesgue, FannIQ, Dancing Chicken, Brawn Media, e outras referências da indústria
> **Referência:** 2025-2026
> **Uso:** Base de conhecimento para análise de audiências no meta-ads-intelligence

---

## 1. Tipos de Audiência

Meta Ads oferece quatro tipos primários de audiência, cada um com um papel diferente no funil:

| Tipo de Audiência | Finalidade | Estágio do Funil |
|---|---|---|
| **Core Audience** (Saved Audience) | Alcançar novas pessoas por demographics, interesses, comportamentos | Topo do funil (ToFu) |
| **Custom Audience** | Fazer retargeting para quem já interagiu com sua marca | Meio/Fundo do funil |
| **Lookalike Audience** | Encontrar novas pessoas semelhantes aos seus melhores clientes | Topo ao meio do funil |
| **Advantage+ Audience** | Deixar a IA da Meta determinar a audiência completa | Todos os estágios (AI-driven) |

### Contexto Estratégico 2025-2026

O modelo antigo (pré-2024) consistia em: o anunciante constrói caixas estreitas de audiência → Meta entrega dentro delas.

O novo modelo (2026): o anunciante fornece sinais de alta qualidade → a IA da Meta determina quem vê os anúncios.

Implicação prática: **a segmentação de audiência é cada vez mais o trabalho do algoritmo. O trabalho do anunciante é fornecer sinais de qualidade (dados primários, pixel/CAPI bem implementado) e criativos de qualidade (que cada vez mais funcionam como mecanismo de segmentação).**

---

### 1.1 Core Audience (Audiência Principal / Saved Audience)

Core Audiences (também chamadas Saved Audiences) são construídas do zero usando dados da plataforma Meta. São a abordagem tradicional de segmentação manual.

**Parâmetros disponíveis:**

- **Localização:** País, região, cidade, CEP, ou raio em torno de um ponto. Opções: pessoas que moram lá, recentemente estiveram lá, ou estão viajando para lá. Restrição hard: localização é um dos únicos parâmetros que o Advantage+ ainda respeita completamente.
- **Idade e Gênero:** Faixa etária de 18 a 65+. Gênero: Todos, Homens, Mulheres. A idade mínima é uma restrição hard em campanhas Advantage+; a idade máxima é apenas uma sugestão.
- **Idiomas:** Segmentar pessoas que usam o Meta em idiomas específicos.
- **Segmentação Detalhada:** Interesses, comportamentos e dados demográficos (ver Seção 2).

**Quando usar Core Audiences:**
- Contas novas sem histórico de pixel ou dados de Custom Audience
- Mercados B2B de nicho com segmentação firmográfica ou por cargo bem definida
- Campanhas geográficas que exigem precisão (ex: raio de 10 km em torno de uma loja)
- Testar hipóteses de segmentação antes de escalar com métodos baseados em IA

**Limitação em 2026:** Os inputs de detailed targeting são tratados como **sugestões por padrão** — a Meta vai além deles para encontrar usuários com melhor desempenho. Apenas localização e idade mínima funcionam como limites reais.

---

### 1.2 Custom Audience (Audiência Personalizada)

Custom Audiences são a segmentação de maior intenção e maior ROI disponível. Permitem alcançar pessoas que já interagiram com seu negócio.

**Limite da conta:** Até 500 Custom Audiences por conta de anúncios.
**Retenção máxima:** 180 dias (exceto vídeo: até 365 dias).

Subtipos principais:
- Website Custom Audience (Pixel + CAPI)
- Customer List (Lista de Clientes)
- App Activity
- Engagement Audiences

(ver Seção 3 para detalhes completos de cada subtipo)

---

### 1.3 Lookalike Audience (Audiência Semelhante)

Lookalike Audiences usam machine learning da Meta para encontrar novas pessoas que estatisticamente se assemelham a uma audiência-fonte — expandindo o alcance para usuários que ainda não interagiram com sua marca.

A Meta analisa os padrões comportamentais e demográficos da sua audiência-fonte e identifica usuários no país/região-alvo que compartilham padrões semelhantes. O algoritmo analisa centenas de sinais, incluindo curtidas em páginas, uso de aplicativos, engajamento com posts, comportamento de compra on/off-platform, consumo de conteúdo e muito mais.

**Tamanhos disponíveis:** 1% a 10% da população do país-alvo.
**Fonte mínima:** 100 pessoas (recomendado: 1.000–5.000 para melhor desempenho).

(ver Seção 4 para detalhes completos)

---

### 1.4 Advantage+ Audience

Advantage+ Audience é o sistema de segmentação baseado em IA da Meta que substitui (ou complementa) o detailed targeting tradicional, Lookalike audiences, e a segmentação de Custom Audience com um único modelo de audiência orientado por machine learning.

A distinção-chave para anunciantes é entender a diferença entre **Controls** (regras hard) e **Suggestions** (guias soft):

- **Audience Controls (Regras Hard):** Localização e idade mínima — esses limites são sempre respeitados.
- **Audience Suggestions (Sinais Soft):** Quando você adiciona sugestões de audiência (Custom Audiences, Lookalikes, interesses, demographics), o sistema prioriza essas audiências antes de buscar mais amplamente — mas pode expandir além delas se identificar usuários com melhor desempenho fora dos parâmetros definidos.

A IA é alimentada pelo Andromeda, uma arquitetura de deep learning introduzida no final de 2024 que processa o comportamento do usuário e faz previsões em tempo real para cada oportunidade de impressão.

(ver Seção 5 para detalhes completos)

---

## 2. Detailed Targeting (Segmentação Detalhada)

### 2.1 Como funciona

Detailed Targeting permite refinar sua audiência dentro do sistema de Core (Saved) Audience usando três categorias: **Demographics**, **Interests** e **Behaviors**.

Encontrado no nível do ad set em "Audience Controls → Detailed Targeting." Você pode:
- **Include** pessoas que correspondem a pelo menos um dos critérios selecionados (lógica OR dentro de uma categoria)
- **Narrow** a audiência (lógica AND — também precisa corresponder a critérios adicionais)
- ~~**Exclude** pessoas~~ — **Removido em 31 de março de 2025** (exclusões por detailed targeting não estão mais disponíveis)

**Mudança crítica de 2025:** Como de 23 de junho de 2025, a Meta começou a consolidar muitas categorias de interesse granulares em agrupamentos mais amplos, com categorias ligadas a esportes, comida, gêneros musicais, modelos de carros e mais sendo fundidas. Adicionalmente, as exclusões de detailed targeting foram removidas.

Em 2026, qualquer input de detailed targeting é uma **sugestão por padrão**. O algoritmo da Meta pode ir além deles para melhorar os resultados.

---

### 2.2 Interesses

Tópicos com que os usuários se engajam com base em seu comportamento na plataforma — páginas curtidas, conteúdo interagido, eventos participados e interesses inferidos.

| Categoria | Exemplos |
|---|---|
| Business & Industry | Empreendedorismo, marketing, imóveis, finanças, tecnologia |
| Entertainment | Filmes, gêneros musicais, programas de TV, games |
| Family & Relationships | Parentalidade, eventos familiares, relacionamentos |
| Fitness & Wellness | Academia, yoga, corrida, nutrição |
| Food & Drink | Culinária, restaurantes, café, vinho |
| Hobbies & Activities | Viagens, fotografia, jardinagem, DIY, esportes |
| Shopping | Moda, beleza, eletrônicos, decoração |
| Technology | Software, gadgets, celulares |

**Aviso importante:** As categorias de interesse foram progressivamente consolidadas desde 2024. Muitos interesses granulares (ex: "fãs de EDM", "proprietários de SUV", "comida vegana") foram fundidos em grupos mais amplos. O inventário de interesses disponíveis continua diminuindo à medida que a Meta aposta em segmentação orientada por IA.

---

### 2.3 Comportamentos

O que os usuários *fazem* — padrões derivados de atividade on-platform, dados de terceiros e uso de dispositivos.

| Subcategoria | Exemplos |
|---|---|
| Digital Activities | Administrador de Facebook Page, proprietário de pequena empresa |
| Mobile Device User | Marca do dispositivo (Apple, Samsung), versão do SO, tipo de conexão (WiFi) |
| Purchase Behavior | Compradores online, compradores de artigos de luxo, compradores empresariais |
| Travel | Viajante internacional frequente, commuter, passageiro frequente |
| Automotive | Compradores de carros por tipo, proprietários de veículos |

---

### 2.4 Dados Demográficos

Quem a pessoa *é* — atributos pessoais estáticos ou semi-estáticos.

| Subcategoria | Exemplos |
|---|---|
| Education | Nível de escolaridade (ensino médio, graduação, pós-graduação), área de estudo |
| Financial | Faixa de renda, faixa de patrimônio líquido |
| Home | Status de proprietário, tipo de moradia, composição familiar |
| Life Events | Mudança recente, novo emprego, noivado recente, novo pai, aniversário próximo |
| Parents | Pais de filhos por faixa etária (0–1 ano, 1–3 anos, etc.) |
| Relationship | Estado civil (solteiro, casado, noivo, em relacionamento) |
| Work | Cargos, empregadores, indústrias |

**Nota sobre segmentação por renda:** A Meta deriva estimativas de renda a partir de dados de CEP e fornecedores de dados de terceiros, não da renda declarada pelo próprio usuário. É uma proxy, não um filtro preciso.

---

### 2.5 Melhores práticas

1. **Adote targeting mais amplo** — em 2025, a abordagem mais eficaz prioriza targeting mais amplo com menos restrições. Adicione 3 a 6 interesses ou comportamentos altamente relevantes como sugestões soft, sem tratá-los como filtros rígidos.

2. **Use Narrowing (AND) para públicos de nicho** — ex: "Interesses: Corrida" E "Demographics: Pais de crianças pequenas" = pais corredores com filhos pequenos.

3. **Use Stacking (OR) para volume** — adicionar múltiplos interesses na mesma caixa fornece um pool maior.

4. **Combine com sinais de primeiro partido** — dado que o detailed targeting é tratado como sugestões, combinar um pequeno número de sinais de interesse de alta relevância com uma estratégia sólida de exclusão de Custom Audiences (clientes adquiridos/existentes) é mais eficaz do que superespecificar com dezenas de tags de interesse.

5. **Confie no algoritmo para escala** — o modelo de targeting Meta 2025 depende de machine learning para construir perfis de usuário probabilísticos com base em grandes volumes de dados comportamentais e de conversão. Quando você alimenta o sistema com sinais fortes de first-party, a Meta começa a criar expansões estilo lookalike em tempo real.

---

## 3. Custom Audiences — Tipos e Configuração

Custom Audiences são construídas a partir de dados que você já possui sobre usuários que interagiram com seu negócio. São a segmentação de maior intenção disponível.

### 3.1 Website Custom Audience (Pixel)

Website Custom Audiences são construídas a partir de pessoas que visitaram seu site, rastreadas via Meta Pixel (browser-side) e/ou Conversions API (server-side).

**Como criar:**
1. Ads Manager → Audiences → Create Audience → Custom Audience → Website
2. Selecione seu Pixel
3. Escolha a condição de evento ou URL (todos os visitantes, visitantes de páginas específicas, ou evento específico)
4. Defina a janela de retenção (1–180 dias)
5. Nomeie e salve a audiência

**Condições de targeting disponíveis:**
- Todos os visitantes do site
- Pessoas que visitaram páginas específicas (URL contains/equals)
- Pessoas que passaram uma quantidade específica de tempo no seu site (top 5%, 10%, 25%)
- Pessoas que completaram eventos específicos (Purchase, AddToCart, InitiateCheckout, ViewContent, Lead, etc.)
- Combinações personalizadas usando lógica AND/OR

**Estratégia por janela de retenção:**

| Janela | Melhor Caso de Uso |
|---|---|
| 1–7 dias | Promoções rápidas, ofertas com prazo, visitantes de maior intenção |
| 8–14 dias | Browsers recentes, retargeting warm |
| 15–30 days | Remarketing padrão, carrinho abandonado |
| 31–60 dias | Produtos de alto ticket com ciclos de decisão mais longos |
| 61–180 dias | Retargeting de brand awareness, nutrição de lead |

**Melhor prática:** Crie audiências separadas para cada janela e segmente as mensagens por recência. Visitantes na janela de 1–7 dias convertem melhor e devem receber criativos mais diretos focados em compra.

---

### 3.2 Customer List (Lista de Clientes)

Faça upload de uma lista de clientes conhecidos e a Meta os combina com perfis de usuários.

**Formatos aceitos:** CSV ou TXT

**Identificadores aceitos (pelo menos um obrigatório):**
- Endereço de e-mail (maior taxa de correspondência)
- Número de telefone (com código do país)
- Nome / Sobrenome
- Data de nascimento
- Gênero
- Cidade, Estado, CEP, País
- Mobile Advertiser ID (MAID)
- Facebook User ID (UID)
- Lead ID (do Meta Lead Ads)

Quanto mais identificadores você fornecer por linha, maior a taxa de correspondência.

**Requisitos de hashing:**
- A Meta aceita valores com hash **SHA-256**, **MD5** ou **valores brutos não hashados**
- Se fizer upload de valores brutos, a Meta faz o hash automático antes de armazenar
- Todos os valores brutos devem usar capitalização consistente (preferência por lowercase)
- Datas devem estar no formato DD-MM-YYYY
- Após a Custom Audience ser criada, todos os dados com hash são deletados dos servidores da Meta

**Melhores práticas:**
- Use sua **lista de clientes com maior LTV** como fonte para Lookalike Audiences
- Segmente listas por lifetime value do cliente, recência ou categoria de produto
- Faça upload de no mínimo 1.000 e-mails para uma audiência significativa; 10.000+ para qualidade de fonte de Lookalike
- Atualize e refaça o upload da sua lista regularmente (mínimo trimestralmente)
- Exclua compradores recentes de campanhas de prospecção para evitar desperdício de orçamento

**Atualização de setembro de 2025:** A Meta bloqueará Custom Audiences (e Lookalike Audiences) que sugiram informações sensíveis, como condições de saúde (ex: "diabetes" ou "artrite") ou status financeiro (ex: "alta renda" ou "score de crédito"). Se sua audiência for sinalizada, pode receber um código de erro (como 471) e não poderá ser usada para veicular anúncios.

---

### 3.3 App Activity

Disponível para empresas com um aplicativo mobile usando o **Meta SDK**.

**Condições de targeting:**
- Todos os usuários que abriram o app
- Usuários mais ativos (top 25%, 10%, 5%)
- Usuários que completaram eventos in-app específicos (Purchase, Level Complete, Content View, etc.)
- Usuários que não abriram o app em um período definido (targeting de re-engajamento)

**Melhores casos de uso:**
- Re-engajar usuários inativos
- Upsell para usuários ativos (ex: usuários que completaram X níveis mas não compraram)
- Excluir clientes pagantes existentes de campanhas de aquisição
- Construir Lookalike Audiences a partir de compradores in-app de alto valor

---

### 3.4 Engagement Audiences

Engagement Custom Audiences são construídas a partir de pessoas que interagiram com seu conteúdo nas plataformas Meta. Representam uma audiência mid-funnel: mais quente do que prospecção fria, mas que ainda não visitou seu site.

| Fonte | O que você pode segmentar |
|---|---|
| **Video** | Assistiu 3s, 10s, 25%, 50%, 75%, 95% de um vídeo específico ou de todos os vídeos |
| **Instagram Account** | Visitou o perfil, engajou com post/anúncio, enviou DM, salvou um post, começou a seguir |
| **Facebook Page** | Visitou a página, engajou com post/anúncio, enviou mensagem, salvou um post |
| **Lead Forms** | Abriu um formulário, abriu mas não enviou, enviou um formulário |
| **Events** | Confirmou presença, demonstrou interesse, interagiu com um Evento |
| **Instant Experience / Canvas** | Abriu ou clicou em uma Instant Experience |
| **Facebook Shop** | Visualizou produtos, adicionou ao carrinho, comprou |
| **AR Experience** | Usou um efeito AR |

**Valor estratégico das Engagement Audiences:**
- Especialmente valiosas para anunciantes sem Meta Pixel (ex: novos negócios)
- Construir pools warm de topo de funil com CPM baixo
- Alimentar Lookalike Audiences quando dados de lista de clientes são limitados
- Mensagens sequenciais: mostrar conteúdo educativo para quem assistiu vídeo, depois ofertas de conversão

---

### 3.5 Qualidade e tamanho mínimo recomendado

- **Tamanho mínimo absoluto:** 100 pessoas para uma Custom Audience
- **Recomendado para bom desempenho:** 500+ pessoas
- **Mínimo para a ferramenta de Audience Overlap funcionar:** 1.000 pessoas
- **Mínimo para fonte de Lookalike Audience:** 100 (mas 1.000–5.000 é recomendado)
- **Ideal para fonte de Lookalike de qualidade:** 10.000+ clientes de alto LTV
- **Retenção máxima:** 180 dias (vídeo: até 365 dias)
- **Limite por conta de anúncios:** até 500 Custom Audiences

---

## 4. Lookalike Audiences

### 4.1 Como criar

1. Ads Manager → Audiences → Create Audience → Lookalike Audience
2. Selecione a **audiência-fonte** (Custom Audience, seguidores da Page ou dados do Pixel)
3. Selecione a **localização-alvo** (país ou região)
4. Defina o **tamanho da audiência** (1%–10% da população)

A Meta analisa os padrões comportamentais e demográficos da sua audiência-fonte e identifica usuários no país/região-alvo que compartilham padrões semelhantes. O algoritmo analisa centenas de sinais, incluindo curtidas em páginas, uso de aplicativos, engajamento com posts, comportamento de compra on/off-platform e consumo de conteúdo.

---

### 4.2 Percentuais (1% a 10%) — o que significam

| Tamanho | Similaridade | Alcance | Recomendado para |
|---|---|---|---|
| **1%** | Mais similar | Menor | Conversões, campanhas focadas em ROAS |
| **2–3%** | Muito similar | Médio | Escalando após 1% ser lucrativo |
| **4–5%** | Similar | Maior | Topo do funil, tráfego, awareness |
| **6–10%** | Mais amplo | Maior | Alcance máximo, testando novos mercados |

**Recomendação de início:** Sempre comece com **1%** para campanhas de conversão. Produz a audiência mais estatisticamente similar e tipicamente entrega o ROAS inicial mais forte.

Dados de desempenho: audiências lookalike de 1% convertendo quase quatro vezes melhor do que lookalikes de 10%, ilustrando o impacto da precisão da audiência.

---

### 4.3 Qualidade da fonte

**A regra mais importante: a qualidade do seu Lookalike é inteiramente determinada pela qualidade da sua audiência-fonte.**

Uma fonte construída a partir de todos os visitantes do site produzirá um Lookalike medíocre. Uma fonte construída a partir dos seus 10% de compradores de maior LTV produzirá um Lookalike altamente direcionado.

**Melhores audiências-fonte (rankeadas por qualidade):**

1. Lista de clientes com maior LTV (top 20% por receita)
2. Evento de Purchase do Pixel (últimos 180 dias)
3. Initiated Checkout ou AddToCart (se compras insuficientes)
4. Atividade de App (compradores in-app)
5. Espectadores de vídeo (75–95% de conclusão)
6. Preenchimentos de lead form
7. Engajadores de Page / conta Instagram
8. Todos os visitantes do site (menor qualidade — use apenas se não houver outros dados)

**Requisitos de tamanho da fonte:**
- **Mínimo:** 100 pessoas na audiência-fonte
- **Recomendado:** 1.000–5.000 pessoas para melhor desempenho
- **Ideal para qualidade:** 10.000+ clientes de alto LTV

---

### 4.4 Quando usar

**Melhores momentos para usar Lookalike Audiences:**
- Expandir para novos mercados além do seu retargeting base
- Prospecção quando você tem dados de conversão sólidos (100+ compradores)
- Escalar campanhas que já provaram eficiência de conversão
- Como sinal (suggestion) dentro de campanhas Advantage+ para dar à IA um ponto de partida de qualidade

**Melhores práticas:**
- **Atualize audiências-fonte trimestralmente** no mínimo; mensalmente para negócios sazonais. Lookalikes refletem automaticamente as atualizações da fonte.
- **Combine múltiplos Lookalikes** em um único ad set uma vez que sejam individualmente comprovados — combine Purchase Lookalike + Video Viewer Lookalike + Engager Lookalike para escala.
- **Exclua suas Custom Audiences** dos ad sets de Lookalike para evitar mostrar anúncios de prospecção para quem já te conhece.
- Não execute mais de 3–5 Lookalike audiences em ad sets separados simultaneamente sem monitoramento de overlap.
- Em 2026, a abordagem mais eficaz é **adicionar Lookalike Audiences como audience suggestions dentro de campanhas Advantage+**, dando ao IA um sinal de qualidade inicial enquanto permite expansão.

---

## 5. Advantage+ Audience

### 5.1 Como funciona

Advantage+ Audience é a configuração de targeting que permite à IA da Meta expandir sua audiência e trata seus inputs como sugestões em vez de regras hard. Em vez de forçar seus anúncios a aparecer apenas para as pessoas específicas que você escolheu, ela usa seus dados para encontrar os melhores clientes em toda a plataforma.

O sistema é alimentado pelo **Andromeda**, uma arquitetura de deep learning introduzida no final de 2024. Os algoritmos de machine learning analisam usuários com base em seus cliques, engajamentos passados e conversões (pixel tracking) na plataforma (tanto no Facebook quanto no Instagram), fazendo previsões em tempo real para cada oportunidade de impressão.

**Diferença vs. targeting manual:**

| Feature | Manual Targeting | Advantage+ Audience |
|---|---|---|
| Controle de audiência | Anunciante define o targeting | IA da Meta determina o alcance |
| Localização | Restrição hard | Restrição hard |
| Idade mínima | Restrição hard | Restrição hard |
| Idade máxima | Restrição hard | Sugestão apenas |
| Gênero | Restrição hard | Sugestão apenas |
| Interesses/Comportamentos | Restrições hard | Sugestões apenas |
| Custom Audiences | Incluídas/excluídas explicitamente | Usadas como sinais |

---

### 5.2 Signals que você pode fornecer

Quando você fornece audience suggestions, o sistema prioriza audiências correspondentes a esse perfil antes de buscar mais amplamente:

- **Custom Audiences** (suas listas de clientes, visitantes do site, engajadores)
- **Lookalike Audiences** (fontes de alta qualidade)
- **Faixa etária** (sugerida, não hard limit exceto idade mínima)
- **Gênero** (sugerido, não hard limit)
- **Localização** (hard limit — sempre respeitado)
- **Interesses e comportamentos** (sugeridos, não hard limits)
- **Demographics** (sugeridos)

**Configuração:**

Ao criar um ad set no Ads Manager:
1. Em "Audience Controls," defina localização e idade mínima (os únicos hard limits)
2. Em "Advantage+ Audience," adicione optional audience suggestions
3. Você pode adicionar Custom Audiences como sugestões — a Meta as priorizará mas pode expandir além delas
4. Deixe outros campos abertos para dar ao IA máxima flexibilidade

---

### 5.3 Vantagens vs targeting manual

**Performance reportada:**
- Até **14,8% de menor custo por resultado** para objetivos de Traffic, Engagement e Leads (dados internos Meta)
- **22% de aumento no ROAS** comparado ao targeting tradicional em estudos internos da Meta (2024)
- **13% de menor custo mediano por venda em catálogo de produto**
- **7% de menor custo mediano por conversão no site**
- **28% de menor custo médio por clique, lead ou page view**
- Desempenho mais consistente quando o pixel tem 50+ eventos de conversão por semana (para sair da fase de aprendizado)

**Quando usar Advantage+ Audience:**
- Contas estabelecidas com histórico rico de pixel e dados de conversão
- E-commerce com catálogo e dados de compra
- Campanhas onde o objetivo é performance ampla e escala
- Quando o criativo é forte e diferenciado (Advantage+ deixa o criativo fazer o targeting)
- Campanhas de escala que já provaram eficiência de conversão

**Quando NÃO usar Advantage+:**
- Públicos B2B muito nichados (total addressable market abaixo de 5.000 pessoas)
- Negócios locais com raio geográfico estreito
- Marcas sem histórico de pixel ou volume muito baixo de conversão
- Verticais sensíveis a compliance onde controle de audiência é legalmente exigido

---

## 6. Estratégia de Funil por Tipo de Audiência

| Estágio do Funil | Tipo de Audiência Recomendado | Abordagem de Criativo |
|---|---|---|
| **Awareness (Topo — ToFu)** | Core Audience (interesses/behaviors amplos), Lookalike 4–10%, Advantage+ | Brand story, problema/solução, conteúdo educativo |
| **Consideration (Meio — MoFu)** | Lookalike 1–3%, Engagement Audiences (video viewers, page engagers) | Social proof, depoimentos, conteúdo educativo de produto |
| **Intent (Alto Meio)** | Website Custom Audience (visitantes de página de produto, últimos 14–30 dias) | Benefícios do produto, objeções respondidas, carrossel de produto |
| **Conversion (Fundo — BoFu)** | Website CA (AddToCart, InitiateCheckout, últimos 3–7 dias), DPA | CTA direto, urgência, desconto, garantia, frete grátis |
| **Retention (Pós-compra)** | Customer List, Past Purchasers CA | Upsell, cross-sell, reorder, acesso VIP, novidades |

### O Funil de Retargeting

```
AWARENESS          VIEWS DE VÍDEO, ENGAJAMENTO COM PAGE/IG
     ↓
CONSIDERATION      VISITANTES DO SITE, LEITORES DE BLOG, CONSUMIDORES DE CONTEÚDO
     ↓
INTENT             VISUALIZADORES DE PÁGINA DE PRODUTO, ADD TO CART, INITIATE CHECKOUT
     ↓
CONVERSION         PURCHASE, SIGN UP, LEAD SUBMIT
     ↓
RETENTION          COMPRADORES ANTERIORES → UPSELL / CROSS-SELL / REORDER
```

### Alocação de Orçamento Recomendada

- **Prospecção (ToFu/MoFu):** 70–80% do orçamento total
- **Retargeting (BoFu):** 20–30% do orçamento total — suficiente para capturar leads quentes sem saturá-los
- **Retenção:** orçamento residual, separado de prospecção

---

## 7. Sobreposição e Exclusões

### 7.1 Audience Overlap Tool

A ferramenta de Audience Overlap da Meta permite verificar a porcentagem de sobreposição entre audiências antes de lançar campanhas.

**Como usar:**
1. Vá para **Ads Manager → Audiences**
2. Selecione **2 ou mais audiências** (até 5 de uma vez) com as caixas de seleção
3. Clique em **"Show Audience Overlap"**
4. A Meta gera um diagrama de Venn mostrando porcentagens de sobreposição

**Requisito:** cada audiência deve ter pelo menos 1.000 pessoas para a ferramenta funcionar.

**Interpretação das porcentagens de sobreposição:**
- Abaixo de 20%: Aceitável — monitore mas nenhuma ação imediata necessária
- 20–30%: Zona de cautela — considere exclusões
- 30–60%: Significativo — implemente exclusões ou consolide
- Acima de 60%: Consolide em um único ad set em vez de excluir

**Por que a sobreposição é prejudicial:**

Quando dois ou mais ad sets segmentam o mesmo usuário, o sistema de leilão de anúncios da Meta os faz competir entre si. Isso resulta em:
- CPMs inflados (você está fazendo lances contra si mesmo)
- Otimização mais lenta do algoritmo (sinais de aprendizado divididos)
- Fadiga acelerada de criativo (o usuário vê a mesma marca duas vezes)
- Dados de atribuição e frequência imprecisos

---

### 7.2 Quando excluir audiências

**Quando excluir é crítico:**

1. **Prospecção vs. Retargeting:** Se uma campanha segmenta novos visitantes do site e outra segmenta compradores anteriores, você deve excluir compradores da campanha de novos visitantes.

2. **Funil ascendente:** Crie um sistema de funil onde cada campanha exclui audiências das campanhas anteriores. Alguém que converte em sua campanha de awareness é excluído das campanhas de consideration.

3. **Lookalikes sobrepostos:** Se dois lookalikes são extraídos da mesma fonte, eles se sobreporão. Se as fontes são similares (instalações vs. visitantes do site), combine ou exclua uma da outra.

---

### 7.3 Boas práticas de exclusão

**Stack padrão de exclusão para campanhas de prospecção:**
- Excluir: Todos os visitantes do site (últimos 30 dias)
- Excluir: Lista de clientes (compradores anteriores)
- Excluir: Enviadores recentes de lead form

**Stack padrão de exclusão para campanhas de retargeting:**
- Excluir: Compradores anteriores (últimos 30–180 dias, dependendo do ciclo de recompra do produto)
- Excluir: Assinantes ativos atuais (se aplicável)

**Mudança de 2025: Detailed Targeting Exclusions removidas**

Em 31 de março de 2025, a Meta removeu a capacidade de excluir pessoas com base em **critérios de detailed targeting** (interesses/comportamentos/demographics). Apenas exclusões de Custom Audience permanecem disponíveis. Isso força todo "negative targeting" baseado em interesses a ser tratado via Custom Audiences.

**Estratégias para corrigir sobreposição de audiência:**

1. **Segmentar por estágio do funil** — manter audiências frias, morna e quentes em campanhas distintas com exclusões únicas e janelas de tempo.

2. **Evitar Lookalike Audiences duplicados** — executar múltiplos lookalikes (como 1% e 2–3%) sem exclusões pode causar grande sobreposição. Combine-os em uma audiência mais ampla ou separe-os cuidadosamente.

3. **Consolidar quando apropriado** — em vez de executar muitos ad sets pequenos com audiências sobrepostas, combine audiências similares (1% + 2% + 3%) em um único ad set.

4. **Monitorar regularmente** — a sobreposição deve ser verificada regularmente, idealmente semanalmente ou a cada lançamento de campanha major.

**Caso de uso real:** Uma marca de e-commerce de beleza estava executando retargeting de visitantes do site em uma campanha e segmentando pessoas que engajaram no Instagram em outra, com 65% de sobreposição de audiência. Após corrigir a sobreposição consolidando em uma campanha e excluindo audiências existentes onde necessário, o custo por compra caiu 37% em apenas duas semanas.

---

## 8. Tamanhos de Audiência Recomendados

O tamanho certo de audiência depende do objetivo da campanha, orçamento e se você está fazendo prospecção ou retargeting.

### Por objetivo

| Objetivo | Tamanho de Audiência Recomendado | Notas |
|---|---|---|
| **Brand Awareness / Reach** | 1M–10M+ | Ampla; o algoritmo otimiza para impressões/alcance |
| **Traffic** | 500K–5M | Precisa de espaço para encontrar clicadores frequentes |
| **Engagement** | 500K–3M | Pool médio; o algoritmo encontra usuários engajados |
| **Lead Generation** | 300K–2M | Equilíbrio entre qualidade e volume |
| **Conversions / Sales** | 100K–2M | O algoritmo precisa de sinais de conversão; muito pequeno = entrega ruim |
| **App Installs** | 500K–5M | Broad targeting frequentemente supera narrow |
| **Video Views** | 1M–10M+ | Pool amplo para entrega de vídeo com custo eficiente |

### Audiências de retargeting

Audiências de retargeting são tipicamente muito menores (1K–100K) e isso é esperado e aceitável. Qualidade > quantidade em retargeting.

**Audiência mínima viável para retargeting:** aproximadamente 1.000 pessoas (a Meta pode restringir a entrega abaixo desse limiar).

### Requisitos da Fase de Aprendizado

- A Meta requer aproximadamente **50 eventos de otimização por ad set por semana** para sair da fase de aprendizado
- Para campanhas de conversão: se sua audiência é muito pequena para gerar 50 eventos de compra por semana, considere:
  - Subir o funil (otimizar para AddToCart ou InitiateCheckout em vez de Purchase)
  - Ampliar a audiência
  - Aumentar o orçamento
  - Consolidar ad sets

### Proporção Orçamento-Audiência

Uma heurística útil: seu orçamento diário deve permitir entrega suficiente para gerar eventos de otimização sem saturar a audiência (fazendo a frequência disparar).

Para audiências de retargeting abaixo de 50K:
- Orçamento diário de R$50–150 (US$10–30) frequentemente é suficiente
- Monitore a frequência semanalmente; se ultrapassar 3–4 em uma semana, renove o criativo ou expanda a audiência

---

## 9. Fontes Oficiais

- [Meta Business Help Center — Detailed Targeting](https://www.facebook.com/business/help/182371508761821)
- [Meta Business Help Center — About Custom Audiences](https://www.facebook.com/business/help/744354708981227)
- [Meta Business Help Center — Create Custom Audience from Website](https://www.facebook.com/business/help/666509013483225)
- [Meta Business Help Center — About Lookalike Audiences](https://www.facebook.com/business/help/164749007013531)
- [Meta Business Help Center — Updates to Detailed Targeting 2025](https://www.facebook.com/business/help/458835214668072)
- [Meta for Business — Advantage+ Audience](https://www.facebook.com/business/ads/meta-advantage-plus/audience)
- [Jon Loomer Digital — Meta Ads Targeting Guide 2025](https://www.jonloomer.com/meta-ads-targeting-guide/)
- [Jon Loomer Digital — Meta Ads Lookalike Audiences](https://www.jonloomer.com/meta-ads-lookalike-audiences/)
- [AdNabu — What Is Meta Advantage+ Audience](https://blog.adnabu.com/facebook/meta-advantage-plus-audience/)
- [TrueFuture Media — Advantage+ Audience How It Works](https://www.truefuturemedia.com/articles/advantage-plus-audience)
- [Brawn Media — How Meta's Targeting Works in 2025](https://brawnmediany.com/blog/how-metas-targeting-works-in-2025-a-complete-guide/)
- [Metalla Digital — Meta Ads Targeting In 2025](https://metalla.digital/meta-ads-targeting-2025/)
- [CropInk — Meta Ads Targeting Options 2026](https://cropink.com/meta-ads-targeting-options)
- [Lebesgue — Broad or Lookalike Audience 2025](https://lebesgue.io/facebook-ads/broad-targeting-beats-lookalikes-the-future-of-facebook-audience-targeting)
- [FannIQ — Meta Detailed Targeting Update 2025](https://www.faniq.live/blog/meta-targeting-update)
- [Turba Media — Broad vs Interest Targeting 2025](https://www.turbamedia.io/post/broad-targeting-vs-interest-targeting---the-definitive-2025-guide)
- [LeadsBridge — Facebook Retargeting Ads 2025](https://leadsbridge.com/blog/facebook-retargeting-ads/)
- [Herd Marketing — Meta Ads Retargeting Funnel](https://www.herdmarketing.co.uk/how-to-build-a-high-performing-retargeting-funnel-on-meta-ads/)
- [BestEver.ai — Audience Overlap 5 Tips 2025](https://www.bestever.ai/post/audience-overlap)
- [Dancing Chicken — How to Exclude Audiences in Meta Ads](https://dancingchicken.com/post/how-to-exclude-audiences-in-meta-ads)
- [Online Optimism — Detailed Targeting Exclusions Update](https://onlineoptimism.com/blog/detailed-targeting-exclusions-in-meta-ad-campaigns/)
- [Segwise — Prevent Audience Overlap 2025](https://segwise.ai/blog/prevent-audience-overlap-ad-campaigns)
- [Chipper — Setup Custom Audiences 2025 Guide](https://chipper.be/blog/how-to-actually-setup-custom-audiences-on-facebook-ads-(2025-guide))
- [Digital Applied — Meta Custom Audience Filters](https://www.digitalapplied.com/blog/meta-custom-audience-filters-retargeting-engagement-frequency)

---

*Synkra AIOS — Meta Ads Intelligence — Knowledge Base*
*Atualizado: março de 2026*
