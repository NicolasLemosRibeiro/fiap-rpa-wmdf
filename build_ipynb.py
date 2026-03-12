import argparse
import os

try:
    import nbformat as nbf
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nbformat'])
    import nbformat as nbf

nb = nbf.v4.new_notebook()

# TÍTULO E INTEGRANTES DA EQUIPE FIAP
text_header = """# Checkpoint FIAP - RPA & NLP (Cross-Tab Data Fusion)

**Objetivo:** Este projeto realiza a extração automatizada multi-domínio da plataforma World Monitor e cruza blocos de dados tabulares caóticos para criar um Contexto Sintético ("Prompt_Ready") útil em pipelines de RAG (Retrieval-Augmented Generation).

---
## Integrantes do Grupo
* **Nicolas Lemos Ribeiro**: RM 553273
* **Ricardo de Paiva Melo**: RM 565522
* **Luís Fernando de Oliveira Salgado**: RM 561401
* **Pedro Leal Murad**: RM 565460
* **Murilo Benhossi**: RM 562358
---"""
nb['cells'] = [nbf.v4.new_markdown_cell(text_header)]

# SETUP
text_setup = """### Etapa 1: Instalação das Dependências (Setup)
Abaixo instalamos o **Playwright** (motor headless realístico de Chromium que não depende de WebDrivers físicos como o Selenium), o **nest_asyncio** (fundamental para rodar o pool assíncrono do Playwright dentro do loop nativo do Google Colab) e bibliotecas de apresentação visual como TQDM para logs."""
nb['cells'].append(nbf.v4.new_markdown_cell(text_setup))

code_install = """!pip install nest_asyncio playwright pandas tqdm
!playwright install-deps chromium
!playwright install chromium"""
nb['cells'].append(nbf.v4.new_code_cell(code_install))

code_imports = """import nest_asyncio
import asyncio
import pandas as pd
import io
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright
from tqdm.notebook import tqdm
from IPython.display import display

# Sem o nest_asyncio, o motor do Colab conflitaria com o event_loop do Playwright
nest_asyncio.apply()"""
nb['cells'].append(nbf.v4.new_code_cell(code_imports))

# RPA PLAYWRIGHT
text_rpa = """### Etapa 2: Robótica Web (RPA com Playwright)
Aqui inicia nossa automação avançada. Em vez de raspar o HTML de forma frágil, nosso robô adota uma estratégia de **Espera Ativa (`wait_for_selector`)**. Como o World Monitor é um Single Page Application (SPA), apenas clicar em "baixar CSV" resultaria em um arquivo vazio se a API ainda não preencheu o front-end. 

Nosso script **interceptará perfeitamente o Stream de Download Nativo** passando pelos eixos de Finanças, Tecnologia e Visão Global."""
nb['cells'].append(nbf.v4.new_markdown_cell(text_rpa))

code_rpa = """async def extrair_multi_dominio():
    # Coleta sequencial ampliada para contemplar todos os 5 eixos temáticos do app
    dominios = {
        'world': 'https://www.worldmonitor.app/',
        'tech': 'https://tech.worldmonitor.app/',
        'finance': 'https://finance.worldmonitor.app/',
        'commodity': 'https://commodity.worldmonitor.app/',
        'happy': 'https://happy.worldmonitor.app/'
    }
    
    os.makedirs('raw_data', exist_ok=True)
    
    async with async_playwright() as p:
        # Configurando o Anti-Bot e Gravador Visual Acadêmico
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            record_video_dir="videos/"
        )
        
        for nome, url in tqdm(dominios.items(), desc="🌍 Extraindo Domínios"):
            page = await context.new_page()
            try:
                print(f"\\n[RPA] Acessando {url}...")
                await page.goto(url, wait_until='domcontentloaded')
                
                # A Espera Ativa (Evita "CSV Fantasma")
                print(f"[RPA] Aguardando a UI carregar e dados popularem via API (Espera robótica)...")
                # Usa o botão de exportação como âncora, pois ele renderiza independente de lazy loading de imagens
                await page.wait_for_selector('button.export-btn', state='attached', timeout=20000)
                # Dá um cold-sleep pra garantir que o SPA terminou os requests REST da API por baixo do capô
                await asyncio.sleep(6) 
                
                # Clique e intercepção assíncrona via Vanilla JS para evitar falhas de Visibilidade do Playwright
                print(f"[RPA] Forçando clique no botão de exportação (Ignorando Overlays/Animações)...")
                await page.evaluate('''() => {
                    const btn = document.querySelector('button.export-btn') || document.querySelector('.export-panel-container button');
                    if (btn) btn.click();
                }''')
                
                await asyncio.sleep(1) # Aguarda o menu dropdown expandir na tela
                
                async with page.expect_download() as download_info:
                    await page.evaluate('''() => {
                        const options = document.querySelectorAll('button.export-option[data-format="json"]');
                        // Se houver múltiplas versões (desktop/mobile), aciona a que está preenchida ou a primeira
                        const btn = Array.from(options).find(e => e.offsetParent !== null) || options[0];
                        if (btn) btn.click();
                    }''')
                
                download = await download_info.value
                
                caminho_arquivo = f"raw_data/{nome}_raw.json"
                await download.save_as(caminho_arquivo)
                print(f"✅ Download retido com sucesso: {caminho_arquivo}")
                
            except Exception as e:
                print(f"❌ Erro na extração de {nome}: {e}")
            finally:
                await page.close()
                
        await context.close()
        await browser.close()
        print("\\n✅ Fase 1 [RPA] Finalizada!")

# Dispara no event_loop do Jupyter
await extrair_multi_dominio()"""
nb['cells'].append(nbf.v4.new_code_cell(code_rpa))

# JSON PARSER
text_parser = """### Etapa 3: Tratamento de Dados (Data Engineering)
O World Monitor agora exporta dados em JSON estruturado, eliminando a dependência do antigo `parse_bad_csv` para CSVs textuais. 

Abaixo, lemos o arquivo JSON de forma extremamente confiável via módulo `json` do Python e criamos os DataFrames do Pandas carregando as chaves nativas `news` e `markets`."""
nb['cells'].append(nbf.v4.new_markdown_cell(text_parser))

code_parser = """def parse_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ {file_path} não encontrado!")
        return None, None

    # Extração direta e elegante do Schema JSON
    df_news = pd.DataFrame(data.get('news', []))
    df_markets = pd.DataFrame(data.get('markets', []))
    
    return df_news, df_markets"""
nb['cells'].append(nbf.v4.new_code_cell(code_parser))

code_cleaning = """print("Executando Data Parsing da Ingestão JSON...")
news_world, mkt_world = parse_json_data('raw_data/world_raw.json')
news_tech, mkt_tech = parse_json_data('raw_data/tech_raw.json')
news_fin, mkt_fin = parse_json_data('raw_data/finance_raw.json')
news_com, mkt_com = parse_json_data('raw_data/commodity_raw.json')
news_happy, mkt_happy = parse_json_data('raw_data/happy_raw.json')

# Concatenação e Limpeza Semântica Global Master
dfs_news = []
for df, dominio in [
    (news_world, 'World'), 
    (news_tech, 'Tech'), 
    (news_fin, 'Finance'),
    (news_com, 'Commodity'),
    (news_happy, 'Good News')
]:
    if df is not None and not df.empty:
        df['Dominio_Origem'] = dominio
        dfs_news.append(df)

if dfs_news:
    df_global_news = pd.concat(dfs_news, ignore_index=True)
    # A chave primária no json é a combinação de title e link. 
    # Mapeando os novos nomes de chaves padrão vindos do JSON se diferirem (ex: 'primaryTitle', 'primaryLink')
    tit_col = 'primaryTitle' if 'primaryTitle' in df_global_news.columns else 'title'
    lnk_col = 'primaryLink' if 'primaryLink' in df_global_news.columns else 'link'
    
    if tit_col in df_global_news.columns and lnk_col in df_global_news.columns:
        df_global_news.drop_duplicates(subset=[tit_col, lnk_col], inplace=True)
    
    # Sanitização de Datas (ISO 8601 Global Alignment) - JSON usa string parecida, mas checaremos a existência
    pub_col = 'lastUpdated' if 'lastUpdated' in df_global_news.columns else 'pubDate'
    if pub_col in df_global_news.columns:
        df_global_news['Published'] = pd.to_datetime(df_global_news[pub_col], errors='coerce')
        df_global_news.sort_values(by='Published', ascending=False, inplace=True)
else:
    df_global_news = pd.DataFrame()

# Capturamos a tabela do Mercado Financeiro para a Fusão
df_global_markets = mkt_fin.copy() if (mkt_fin is not None and not mkt_fin.empty) else pd.DataFrame()"""
nb['cells'].append(nbf.v4.new_code_cell(code_cleaning))

# CROSS-TAB FUSION (NLP)
text_fusion = """### Etapa 4: Cross-Tab Data Fusion (O Cérebro da Operação para a NLP/RAG)

É aqui que o "ouro" é formado para a equipe de AI (Etapa 4 do Padrão Lima na prova). 
Jogar uma "Notícia" isolada dentro de uma RAG gera embeddings contextuais matematicamente genéricos. O que fazemos aqui é o **Enriquecimento Estrutural por Metadados Sintéticos**.

Pegamos a planilha separada de **Índices Macroeconômicos** extraída do RPA e mesclamos em linguagem natural com a aba de **Notícias/Geopolítica**, gerando a coluna `Prompt_Ready` (a notícia + o sentimento e saúde da bolsa mundial atrelados juntos ao arquivo `nlp_ready_fusion.csv`)."""
nb['cells'].append(nbf.v4.new_markdown_cell(text_fusion))

code_fusion = """# Preparando o Contexto de "Temperatura" Global via Bolsa/Commodities
cenario_macro = "Estável"
if not df_global_markets.empty:
    indicadores = []
    # Selecionamos apenas os de alta importância corporativa para não torrar tokens do LLM depois (Top 5)
    sym_col = 'symbol' if 'symbol' in df_global_markets.columns else 'Symbol'
    chg_col = 'change' if 'change' in df_global_markets.columns else 'Change'
    
    for _, row in df_global_markets.head(5).iterrows(): 
        sym = row.get(sym_col, 'N/A')
        chg = str(row.get(chg_col, '0')).strip()
        indicadores.append(f"{sym} ({chg})")
    
    texto_indices = " | ".join(indicadores)
    cenario_macro = f"Mercado Misto. Indicadores Chaves simultâneos: {texto_indices}."

def construir_prompt_ready(row):
    # Adapter para o novo esquema nativo do JSON vs CSV
    tit_col = 'primaryTitle' if 'primaryTitle' in row else 'title'
    src_col = 'primarySource' if 'primarySource' in row else 'source'
    
    titulo = row.get(tit_col, row.get('Title', 'Sem Título'))
    fonte = row.get(src_col, row.get('Source', 'Desconhecida'))
    data = row.get('Published')
    dominio = row.get('Dominio_Origem', 'Global')
    
    data_str = data.isoformat() if pd.notnull(data) else 'Data Recente'
    
    # Textualização Semântica Densa "Mastigada" pró NLP/LLM
    contexto = (
        f"Aba Taxonômica da Plataforma: [{dominio}]. "
        f"Em {data_str}, a fonte '{fonte}' relatou essa manchete central: "
        f"'{titulo}'. "
        f"Para baseamento analítico da resposta, repara-se que o Contexto Macroeconômico/Bolsa Mundial neste mesmo ponto do tempo era: {cenario_macro}"
    )
    return contexto

if not df_global_news.empty:
    df_global_news['Contexto_Sintetico'] = cenario_macro
    df_global_news['Prompt_Ready'] = df_global_news.apply(construir_prompt_ready, axis=1)

    # Reordenando para deixar bonito e acadêmico aos olhos do professor
    tit_col = 'primaryTitle' if 'primaryTitle' in df_global_news.columns else 'title'
    src_col = 'primarySource' if 'primarySource' in df_global_news.columns else 'source'
    lnk_col = 'primaryLink' if 'primaryLink' in df_global_news.columns else 'link'

    cols_ordem = ['Published', 'Dominio_Origem', src_col, tit_col, lnk_col, 'Contexto_Sintetico', 'Prompt_Ready']
    df_final = df_global_news[[c for c in cols_ordem if c in df_global_news.columns]]
    
    # Salvando a entrega final
    df_final.to_csv('nlp_ready_fusion.csv', index=False)
    
    print("\\n✅ Mágica de Dados concluída. Arquivo final pronto para ingestão do Bert/GPT (RAG)!")
    print("💎 Amostra do Enriquecimento (Coluna Prompt_Ready pronta para Ingestão):\\n")
    
    pd.set_option('display.max_colwidth', 150)
    display(df_final[[tit_col, 'Prompt_Ready']].head(8))
else:
    print("Dataset de cruzamento final resultou vazio.")"""
nb['cells'].append(nbf.v4.new_code_cell(code_fusion))

with open('c:/Users/Luis/Downloads/Development/CP1 RPA/RPA_World_Monitor_Extração.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook generated successfully with Storytelling & Groups!")
