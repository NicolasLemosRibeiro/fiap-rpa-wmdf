# Checkpoint FIAP — RPA & NLP (Cross-Tab Data Fusion + Análise de Sentimentos)

**Objetivo:** Pipeline automatizado que extrai dados da plataforma World Monitor via RPA, aplica análise de sentimentos com BERT e gera um relatório analítico com Google Gemini (RAG).

**Integrantes:**

| Nome | RM |
|------|-----|
| Nicolas Lemos Ribeiro | 553273 |
| Ricardo de Paiva Melo | 565522 |
| Luís Fernando de Oliveira Salgado | 561401 |
| Pedro Leal Murad | 565460 |
| Murilo Benhossi | 562358 |

---

## Arquitetura do Projeto

```
fiap-rpa-wmdf/
│
├── RPA_World_Monitor_Extração.ipynb       # Etapa 1-2: RPA + Data Engineering
├── NLP_Sentimentos_Resumo_Analitico.ipynb # Etapa 3-4: NLP + Resumo Analítico (RAG)
├── index.html                              # Dashboard interativo (Intel Fusion Hub)
│
├── output/
│   ├── nlp_ready_fusion.csv                # Saída RPA: dataset intermediário (RPA → NLP)
│   ├── resultado_sentimentos.csv           # Saída NLP: CSV com sentimentos classificados
│   └── relatorio_analitico.md              # Saída NLP: Relatório gerado pelo Gemini
│
├── raw_data/
│   ├── world_raw.json
│   ├── tech_raw.json
│   ├── finance_raw.json
│   ├── commodity_raw.json
│   └── happy_raw.json
│
└── PRIMEIRO CHECKPOINT NLP & RPA_final.pdf
```

---

## Pipeline (Fluxo de Execução)

### Etapa 1 — Coleta de Dados (RPA)
**Notebook:** `RPA_World_Monitor_Extração.ipynb`

- Automação com **Playwright** (Chromium headless) na plataforma World Monitor
- **Dupla Estratégia de Extração:**
  1. **DOM Scraping** — captura manchetes dos painéis renderizados da SPA
  2. **JSON Export** — download nativo para Markets e Predictions (Polymarket)
- Coleta de **5 domínios:** World, Tech, Finance, Commodity, Good News

### Etapa 2 — Preparação dos Dados (RPA)
**Notebook:** `RPA_World_Monitor_Extração.ipynb`

- Parse dos JSONs brutos (news + markets + predictions)
- **Cross-Tab Data Fusion:** enriquecimento com contexto macroeconômico
- Geração da coluna `Prompt_Ready` (texto + contexto da bolsa)
- **Saída:** `output/nlp_ready_fusion.csv` (~297 registros)

### Etapa 3 — Análise de Sentimentos (NLP)
**Notebook:** `NLP_Sentimentos_Resumo_Analitico.ipynb`

- Pré-processamento: remoção de prefixos, normalização, stopwords
- Modelo: **`nlptown/bert-base-multilingual-uncased-sentiment`** (HuggingFace)
- Classificação: Positivo (4-5★) / Neutro (3★) / Negativo (1-2★)
- Visualizações: distribuição, sentimento por domínio, wordclouds, confiança
- **Saída:** `resultado_sentimentos.csv`

### Etapa 4 — Resumo Analítico com RAG (NLP)
**Notebook:** `NLP_Sentimentos_Resumo_Analitico.ipynb`

- **RAG (Retrieval-Augmented Generation):**
  1. Recuperação dos dados reais (estatísticas, manchetes, palavras-chave)
  2. Montagem de prompt enriquecido com contexto do dataset
  3. Geração com **Google Gemini 2.5 Flash Lite**
- Relatório com: panorama geral, análise por domínio, riscos, oportunidades e recomendações
- **Saída:** `relatorio_analitico.md`

### Visualização — Dashboard (index.html)

- Dashboard **Intel Fusion Hub** com TailwindCSS + Chart.js
- Aceita upload manual de `resultado_sentimentos.csv` e `relatorio_analitico.md` (disponíveis na pasta `output/`)
- Gráficos: donut de sentimentos, barras por domínio, confiança BERT
- Tabela filtrável com busca, badges de sentimento e estrelas
- Relatório analítico renderizado em Markdown

---

## Como Executar

### 1. Notebook RPA (Google Colab)
1. Abrir `RPA_World_Monitor_Extração.ipynb` no Google Colab
2. Executar todas as células sequencialmente
3. Baixar o arquivo `output/nlp_ready_fusion.csv` gerado

### 2. Notebook NLP (Google Colab)
1. Abrir `NLP_Sentimentos_Resumo_Analitico.ipynb` no Google Colab
2. Fazer upload do `nlp_ready_fusion.csv` quando solicitado
3. Configurar a API Key do Google Gemini (gratuita via [AI Studio](https://aistudio.google.com/apikey))
4. Executar todas as células sequencialmente
5. Baixar `resultado_sentimentos.csv` e `relatorio_analitico.md`

### 3. Dashboard (Navegador)
1. Abrir `index.html` no navegador
2. Fazer upload do `resultado_sentimentos.csv`
3. Fazer upload do `relatorio_analitico.md`
4. Os dados e o relatório são exibidos automaticamente

---

## Domínios Extraídos

| Domínio | URL | Conteúdo |
|---------|-----|----------|
| World | worldmonitor.app | Geopolítica, conflitos, diplomacia |
| Tech | tech.worldmonitor.app | IA/ML, cibersegurança, inovação |
| Finance | finance.worldmonitor.app | Mercados financeiros, economia |
| Commodity | commodity.worldmonitor.app | Commodities, energia, agricultura |
| Good News | happy.worldmonitor.app | Notícias positivas, avanços sociais |

---

## Stack Tecnológica

| Componente | Tecnologia |
|-----------|------------|
| RPA | Playwright (Chromium headless) + asyncio |
| Data Engineering | Pandas, JSON parsing |
| NLP - Sentimentos | HuggingFace Transformers (BERT multilíngue) |
| NLP - Resumo (RAG) | Google Gemini 2.5 Flash Lite |
| Frontend | TailwindCSS, Chart.js, PapaParse, Marked.js, Lucide Icons |
| Ambiente | Google Colab |

---

## Resultados

- **297 textos** analisados de 5 domínios
- **54.9% Positivos** | **3.0% Neutros** | **42.1% Negativos**
- Domínio mais positivo: **Good News** (66.7%)
- Domínio mais negativo: **Commodity** (51.9%)
- Relatório com recomendações estratégicas para equipe de marketing

---

*Checkpoint FIAP 2026 — NLP, Chatbots e Agentes Virtuais + RPA*
