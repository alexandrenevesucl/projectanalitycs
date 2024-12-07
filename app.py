import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt

# Carregar os dados
file_path = "dados_roubos.csv"
df = pd.read_csv(file_path)

# Pré-processamento
df['DATA DO FATO'] = pd.to_datetime(df['DATA DO FATO'], errors='coerce')
df['HORA DO FATO'] = pd.to_datetime(df['HORA DO FATO'], format='%H:%M:%S', errors='coerce').dt.time

# Funções de visualização
def top_bairros(municipio, tipo_incidente, tipo_local):
    filtro = df
    if municipio:
        filtro = filtro[filtro['MUNICÍPIO'] == municipio]
    if tipo_incidente:
        filtro = filtro[filtro['TIPO DE INCIDENTE'] == tipo_incidente]
    if tipo_local:
        filtro = filtro[filtro['TIPO DE LOCAL'] == tipo_local]
    
    top_bairros = filtro['BAIRRO'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_bairros.plot(kind='bar', ax=ax, color='lightcoral', edgecolor='black')
    ax.set_title(f'Top 10 Bairros com Mais Roubos', fontsize=16)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.set_xlabel('Bairro', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def roubos_por_horario(municipio, tipo_incidente, tipo_local):
    filtro = df
    if municipio:
        filtro = filtro[filtro['MUNICÍPIO'] == municipio]
    if tipo_incidente:
        filtro = filtro[filtro['TIPO DE INCIDENTE'] == tipo_incidente]
    if tipo_local:
        filtro = filtro[filtro['TIPO DE LOCAL'] == tipo_local]
    
    horarios = filtro['HORA DO FATO'].dropna().astype(str).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    horarios.plot(kind='line', ax=ax, marker='o', color='blue')
    ax.set_title('Distribuição de Roubos por Horário', fontsize=16)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.set_xlabel('Horário', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def tipos_de_incidente(municipio, tipo_incidente, tipo_local):
    # Filtrar os dados com base nos filtros selecionados
    filtro = df
    if municipio:
        filtro = filtro[filtro['MUNICÍPIO'] == municipio]
    if tipo_incidente:
        filtro = filtro[filtro['TIPO DE INCIDENTE'] == tipo_incidente]
    if tipo_local:
        filtro = filtro[filtro['TIPO DE LOCAL'] == tipo_local]

    # Remover a nomenclatura "CRIMES CONTRA O PATRIMÔNIO:" dos tipos de incidente
    filtro['TIPO DE INCIDENTE'] = filtro['TIPO DE INCIDENTE'].str.replace(r'^CRIMES CONTRA O PATRIMÔNIO: ', '', regex=True)

    # Contar os tipos de incidente
    tipos = filtro['TIPO DE INCIDENTE'].value_counts()

    # Criar o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    tipos.plot(kind='bar', ax=ax, color='darkorange', edgecolor='black')
    ax.set_title('Distribuição Percentual por Tipos de Incidente', fontsize=16)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.set_xlabel('Tipo de Incidente', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def distribuicao_por_tipo_local(municipio, tipo_incidente, tipo_local):
    filtro = df
    if municipio:
        filtro = filtro[filtro['MUNICÍPIO'] == municipio]
    if tipo_incidente:
        filtro = filtro[filtro['TIPO DE INCIDENTE'] == tipo_incidente]
    if tipo_local:
        filtro = filtro[filtro['TIPO DE LOCAL'] == tipo_local]
    
    locais = filtro['TIPO DE LOCAL'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    locais.plot(kind='bar', ax=ax, color='purple', edgecolor='black')
    ax.set_title('Distribuição por Tipo de Local', fontsize=16)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.set_xlabel('Tipo de Local', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Interface Gradio
def interface(municipio, tipo_incidente, tipo_local):
    fig1 = top_bairros(municipio, tipo_incidente, tipo_local)
    fig2 = roubos_por_horario(municipio, tipo_incidente, tipo_local)
    fig3 = tipos_de_incidente(municipio, tipo_incidente, tipo_local)
    fig4 = distribuicao_por_tipo_local(municipio, tipo_incidente, tipo_local)
    return fig1, fig2, fig3, fig4

municipios_unicos = [''] + sorted(df['MUNICÍPIO'].dropna().unique())
tipos_incidente_unicos = [''] + sorted(df['TIPO DE INCIDENTE'].dropna().unique())
tipos_local_unicos = [''] + sorted(df['TIPO DE LOCAL'].dropna().unique())

gr.Interface(
    fn=interface,
    inputs=[
        gr.Dropdown(label='Selecione um Município', choices=municipios_unicos, value=''),
        gr.Dropdown(label='Selecione um Tipo de Incidente', choices=tipos_incidente_unicos, value=''),
        gr.Dropdown(label='Selecione um Tipo de Local', choices=tipos_local_unicos, value='')
    ],
    outputs=[
        gr.Plot(label='Top 10 Bairros com Mais Roubos'),
        gr.Plot(label='Distribuição de Roubos por Horário'),
        gr.Plot(label='Distribuição Percentual de Tipos de Incidente'),
        gr.Plot(label='Distribuição por Tipo de Local')
    ],
    live=True,
    title='Análise de Ocorrências de Roubos no Espírito Santo',
    description='Use os filtros para explorar dados por município, tipo de incidente e tipo de local.'
).launch()