# Checkpoint FIAP - RPA & NLP (Cross-Tab Data Fusion)

**Objetivo:** Extração automatizada multi-domínio da plataforma [World Monitor](https://www.worldmonitor.app/) com cruzamento de dados tabulares (News + Markets + Predictions) para gerar um Contexto Sintético ("Prompt_Ready") consumível por pipelines de RAG (Retrieval-Augmented Generation).

## Arquitetura do Projeto

```
├── RPA_World_Monitor_Extração.ipynb   # Engine principal (RPA + Data Engineering + Fusão)
├── index.html                         # Dashboard interativo (Intel Fusion Hub)
├── output/
│   └── nlp_ready_fusion.csv           # Dataset enriquecido final (Prompt_Ready para LLMs)
├── raw_data/                          # Cache dos JSONs brutos por domínio
│   ├── world_raw.json
│   ├── tech_raw.json
│   ├── finance_raw.json
│   ├── commodity_raw.json
│   └── happy_raw.json
└── PRIMEIRO CHECKPOINT NLP & RPA_final.pdf  # Documentação acadêmica
```

### Componentes

- **`RPA_World_Monitor_Extração.ipynb`** — Notebook que roda toda a pipeline: instalação de dependências, automação com Playwright (headless Chromium), parseamento JSON e fusão de dados. Utiliza uma **Dupla Estratégia de Extração**:
  1. **DOM Scraping** — Percorre os painéis renderizados da SPA para capturar manchetes que o export JSON não inclui (World, Tech, Finance).
  2. **JSON Export** — Download nativo para capturar dados de Markets (índices financeiros) e Predictions (Polymarket), além de news já preenchidas (Commodity, Good News).
  3. **Merge inteligente** — Unifica as duas fontes com deduplicação por título.

- **`index.html`** — Dashboard "Intel Fusion Hub" construído com TailwindCSS + Chart.js. Permite file-upload do `nlp_ready_fusion.csv` e exibe indicadores numéricos, gráficos de distribuição por domínio, linha do tempo e listagem completa das notícias.

- **`output/nlp_ready_fusion.csv`** — Arquivo final enriquecido com a coluna `Prompt_Ready`, que combina a manchete original com o contexto macroeconômico da bolsa mundial no mesmo instante temporal. Inclui tanto **News** quanto **Predictions** (Polymarket), diferenciados pela coluna `Tipo_Conteudo`.

- **`raw_data/`** — JSONs brutos extraídos dos 5 domínios, contendo as chaves `news`, `markets` e `predictions`.

## Domínios Extraídos

| Domínio | URL | Conteúdo |
|---------|-----|----------|
| World | worldmonitor.app | Geopolítica, conflitos, diplomacia |
| Tech | tech.worldmonitor.app | IA/ML, cibersegurança, inovação |
| Finance | finance.worldmonitor.app | Mercados financeiros, economia |
| Commodity | commodity.worldmonitor.app | Commodities, energia, agricultura |
| Good News | happy.worldmonitor.app | Notícias positivas, avanços sociais |

## Como Executar

1. Abrir `RPA_World_Monitor_Extração.ipynb` no Google Colab ou Jupyter
2. Executar todas as células sequencialmente — o notebook instala as dependências automaticamente (`playwright`, `nest_asyncio`, `pandas`, `tqdm`)
3. O output será gerado em `output/nlp_ready_fusion.csv`
4. Para visualizar, abrir `index.html` no navegador e fazer upload do CSV

## Observações Técnicas (Volumetria e Temporalidade)

1. **Volume de Dados (~250-260 registros únicos):** O arquivo final consolida em média 257 registros entre News e Predictions. Limites de paginação da API (~Top 50 por eixo) e deduplicação (`drop_duplicates`) determinam esse volume.

2. **Intervalo Temporal Amplo:** A janela analítica abrange em média **5 meses** de notícias latentes, oferecendo profundidade para treino de ML.

3. **Estabilidade entre Execuções:** Execuções no mesmo dia produzem outputs idênticos, atestando a estabilidade do motor RPA.

4. **News Vazias em Alguns Domínios:** O export JSON dos domínios World, Tech e Finance retorna `"news": []` — isso é uma limitação da API, não um bug. A **Dupla Estratégia** (DOM Scraping) compensa essa limitação extraindo as manchetes diretamente dos painéis renderizados.

5. **Dados de Mercado (Oportunidades Futuras):** Endpoints com `"news"` vazias trazem dados ricos em `"markets"` (tickers, preços, variações), abrindo caminho para um futuro `market_tickers.csv` para algoritmos de trading.

## Stack Tecnológica

- **RPA:** Playwright (Chromium headless) + asyncio
- **Data Engineering:** Pandas, JSON parsing
- **Frontend:** TailwindCSS, Chart.js, PapaParse, Lucide Icons
- **Ambiente:** Google Colab / Jupyter Notebook

## Integrantes do Grupo

| Nome | RM |
|------|-----|
| Nicolas Lemos Ribeiro | 553273 |
| Ricardo de Paiva Melo | 565522 |
| Luís Fernando de Oliveira Salgado | 561401 |
| Pedro Leal Murad | 565460 |
| Murilo Benhossi | 562358 |
