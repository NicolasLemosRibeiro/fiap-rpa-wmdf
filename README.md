# Checkpoint FIAP - RPA & NLP (Cross-Tab Data Fusion)

**Objetivo:** Este projeto realiza a extração automatizada multi-domínio da plataforma [World Monitor](https://www.worldmonitor.app/) e cruza blocos de dados tabulares caóticos para criar um Contexto Sintético ("Prompt_Ready") útil em pipelines de RAG (Retrieval-Augmented Generation).

## Arquitetura do Projeto
- `build_ipynb.py`: Script Python responsável pela orquestração. Instala dependências e gera o notebook localmente, extraindo os dados em tempo real utilizando RPA assíncrono com Playwright.
- `RPA_World_Monitor_Extração.ipynb`: Notebook final exportado que roda toda a engine de extração, parseamento JSON e fusão de dados.
- `index.html`: Dashboard interativo moderno desenhado com TailwindCSS que consome o dataset transacionado, permitindo o file-upload (`nlp_ready_fusion.csv`) com indicadores numéricos de monitoramento, linha do tempo e status sintético visual do fechamento das bolsas.
- `output/nlp_ready_fusion.csv`: Arquivo final enriquecido, o "Ouro", já em um formato consumível para Large Language Models (LLMs) lerem como Contexto.
- `raw_data/`: (Gerado em tempo de execução) Cache dos JSONs puros recém extraídos.

## Observações Técnicas Importantes (Volumetria e Temporalidade)
Ao analisar o output gerado por nosso motor RPA e os dados fundidos no arquivo `nlp_ready_fusion.csv`, notamos os seguintes comportamentos determinísticos:

1. **Volume de Dados (Aprox. 250 a 260 linhas únicas):** Apesar de termos múltiplas fontes contínuas (World, Tech, Finance, Commodity, Good News), o arquivo final consolida em média 257 registros consolidados. Isso ocorre por duas razões técnicas:
   - **Limites de Payload da API (Paginação):** Portais de notícias e APIs do World Monitor limitam o primeiro request às Top N notícias mais relevantes de cada categoria para otimização de performance. (ex: 5 eixos temáticos x Top 50 = ~250 registros). 
   - **Data Cleaning Integrado:** Durante nosso pipeline, o script aplica rotinas de desduplicação (`drop_duplicates`). Se a mesma manchete aparece categorizada tanto em "Tech" quanto em "World", nossa engenharia a unifica, evitando tokens desperdiçados no Prompt RAG.
2. **Intervalo Temporal Amplo (Time Range):** A janela analítica extraída não se restringe a 24 horas ou 7 dias. Os metadados temporais presentes nas notícias apontam abrangências históricas de em média **5 meses** (Ex: *Outubro de 2025 a Março de 2026*), consistindo em excelente profundidade para treino de Machine Learning, uma vez que capturamos as "Braking News" mais latentes nesse espaço de tempo.
3. **Dados Estáticos (Testes de Execução):** Em execuções sucessivas do Crawler no mesmo dia num ambiente de simulação, o output de geração dos gráficos resultará idêntico. Isso atesta a estabilidade rigorosa da rotina RPA – pois a fonte da API em si se manteve sem novas atualizações no intermédio da execução.

## Integrantes do Grupo
* **Nicolas Lemos Ribeiro**: RM 553273
* **Ricardo de Paiva Melo**: RM 565522
* **Luís Fernando de Oliveira Salgado**: RM 561401
* **Pedro Leal Murad**: RM 565460
* **Murilo Benhossi**: RM 562358
