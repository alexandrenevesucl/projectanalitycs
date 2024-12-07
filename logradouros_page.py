import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt

# Carregar os dados
file_path = "dados_roubos.csv"  # Certifique-se de usar o mesmo arquivo de dados
df = pd.read_csv(file_path)

# Pré-processamento
df['DATA DO FATO'] = pd.to_datetime(df['DATA DO FATO'], errors='coerce')
df['HORA DO FATO'] = pd.to_datetime(df['HORA DO FATO'], format='%H:%M:%S', errors='coerce').dt.time

# Funções de visualização
def ruas_por_bairro(municipio, bairro, tipo_incidente, tipo_local):
    filtro = df[(df['MUNICÍPIO'] == municipio) & (df['BAIRRO'] == bairro)]
    if tipo_incidente:  # Aplica o filtro de tipo de incidente, se selecionado
        filtro = filtro[filtro['TIPO DE INCIDENTE'] == tipo_incidente]
    if tipo_local:  # Aplica o filtro de tipo de local, se selecionado
        filtro = filtro[filtro['TIPO DE LOCAL'] == tipo_local]
    top_ruas = filtro['LOGRADOURO'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_ruas.plot(kind='bar', ax=ax, color='green', edgecolor='black')
    ax.set_title(f'Top 10 Logradouros com Mais Roubos em {bairro} ({municipio})', fontsize=16)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.set_xlabel('Logradouro', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def horarios_por_bairro(municipio, bairro, tipo_incidente, tipo_local):
    filtro = df[(df['MUNICÍPIO'] == municipio) & (df['BAIRRO'] == bairro)]
    if tipo_incidente:  # Aplica o filtro de tipo de incidente, se selecionado
        filtro = filtro[filtro['TIPO DE INCIDENTE'] == tipo_incidente]
    if tipo_local:  # Aplica o filtro de tipo de local, se selecionado
        filtro = filtro[filtro['TIPO DE LOCAL'] == tipo_local]
    horarios = filtro['HORA DO FATO'].dropna().astype(str).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    horarios.plot(kind='line', ax=ax, marker='o', color='blue')
    ax.set_title(f'Distribuição de Horários de Roubos em {bairro} ({municipio})', fontsize=16)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.set_xlabel('Horário', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Interface Gradio
def logradouro_interface(municipio, bairro, tipo_incidente, tipo_local):
    if not municipio or not bairro:
        return None, None
    fig1 = ruas_por_bairro(municipio, bairro, tipo_incidente, tipo_local)
    fig2 = horarios_por_bairro(municipio, bairro, tipo_incidente, tipo_local)
    return fig1, fig2

municipios_unicos = [''] + sorted(df['MUNICÍPIO'].dropna().unique())

def atualizar_bairros(municipio):
    if municipio:
        bairros = [''] + sorted(df[df['MUNICÍPIO'] == municipio]['BAIRRO'].dropna().unique())
    else:
        bairros = ['']
    return gr.update(choices=bairros, value='')

def atualizar_tipos_incidente(municipio, bairro):
    if municipio and bairro:
        tipos_incidente = [''] + sorted(df[(df['MUNICÍPIO'] == municipio) & (df['BAIRRO'] == bairro)]['TIPO DE INCIDENTE'].dropna().unique())
    else:
        tipos_incidente = ['']
    return gr.update(choices=tipos_incidente, value='')

def atualizar_tipos_local(municipio, bairro):
    if municipio and bairro:
        tipos_local = [''] + sorted(df[(df['MUNICÍPIO'] == municipio) & (df['BAIRRO'] == bairro)]['TIPO DE LOCAL'].dropna().unique())
    else:
        tipos_local = ['']
    return gr.update(choices=tipos_local, value='')

with gr.Blocks(title="Análise por Logradouros") as logradouros_page:
    gr.Markdown("# Página de Logradouros")
    
    # Dropdowns de seleção
    municipio = gr.Dropdown(label="Selecione o Município", choices=municipios_unicos, value="")
    bairro = gr.Dropdown(label="Selecione o Bairro", choices=[''], value="")
    tipo_incidente = gr.Dropdown(label="Selecione o Tipo de Incidente (Opcional)", choices=[''], value="")
    tipo_local = gr.Dropdown(label="Selecione o Tipo de Local (Opcional)", choices=[''], value="")
    
    # Atualizações dinâmicas
    municipio.change(atualizar_bairros, inputs=[municipio], outputs=[bairro])
    bairro.change(atualizar_tipos_incidente, inputs=[municipio, bairro], outputs=[tipo_incidente])
    bairro.change(atualizar_tipos_local, inputs=[municipio, bairro], outputs=[tipo_local])
    
    # Botão e gráficos
    botao_exibir = gr.Button("Exibir Gráficos")
    output1 = gr.Plot(label="Top 10 Logradouros com Mais Roubos")
    output2 = gr.Plot(label="Distribuição de Horários de Roubos")
    
    botao_exibir.click(logradouro_interface, inputs=[municipio, bairro, tipo_incidente, tipo_local], outputs=[output1, output2])

logradouros_page.launch()
