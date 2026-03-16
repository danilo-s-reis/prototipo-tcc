import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import json

# Conexão com o Banco de Dados
DATABASE_URL = "sqlite:///job_data_pipeline.db"
engine = create_engine(DATABASE_URL)

def load_data():
    """Carrega os dados das tabelas 'vagas' e 'habilidades'."""
    with engine.connect() as connection:
        # Carregar vagas
        vagas_query = text("SELECT * FROM vagas")
        df_vagas = pd.read_sql(vagas_query, connection)
        
        # Carregar habilidades
        habilidades_query = text("SELECT * FROM habilidades")
        df_habilidades = pd.read_sql(habilidades_query, connection)
        
    # Deserializar o JSON para a descrição completa
    df_vagas['descricao_completa'] = df_vagas['detalhes_json'].apply(lambda x: json.loads(x).get('descricao_completa', ''))
    
    # Merge dos DataFrames
    df_merged = pd.merge(df_vagas, df_habilidades, left_on='id', right_on='vaga_id', how='left')
    
    return df_merged, df_vagas, df_habilidades

# --- Configuração do Dashboard ---
st.set_page_config(layout="wide", page_title="Protótipo de Dashboard de Vagas de TI")

st.title("📊 Protótipo de Dashboard de Vagas de TI")
st.markdown("Demonstração das visualizações interativas baseadas nos requisitos (RF-011 a RF-015).")

df_merged, df_vagas, df_habilidades = load_data()

# --- RF-013: Filtros Interativos ---
st.sidebar.header("Filtros Interativos (RF-013)")

# Filtro de Título do Cargo
titulos = ['Todos'] + sorted(df_vagas['titulo'].unique().tolist())
filtro_titulo = st.sidebar.selectbox("Título do Cargo", titulos)

# Filtro de Localização
localizacoes = ['Todas'] + sorted(df_vagas['localizacao'].unique().tolist())
filtro_localizacao = st.sidebar.selectbox("Localização", localizacoes)

# Filtro de Nível de Senioridade
senioridades = ['Todos'] + sorted(df_habilidades['nivel_senioridade'].dropna().unique().tolist())
filtro_senioridade = st.sidebar.selectbox("Nível de Senioridade", senioridades)

# Filtro de Modalidade
modalidades = ['Todas'] + sorted(df_vagas['modalidade'].unique().tolist())
filtro_modalidade = st.sidebar.selectbox("Modalidade", modalidades)

# Aplicação dos Filtros
df_filtrado = df_merged.copy()

if filtro_titulo != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['titulo'] == filtro_titulo]
if filtro_localizacao != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['localizacao'] == filtro_localizacao]
if filtro_senioridade != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['nivel_senioridade'] == filtro_senioridade]
if filtro_modalidade != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['modalidade'] == filtro_modalidade]

# Garante que o DataFrame de vagas filtradas não tenha duplicatas de vagas
df_vagas_filtradas = df_filtrado.drop_duplicates(subset=['id_x'])

# --- RF-011: Indicadores Chave de Desempenho ---
st.header("Indicadores Chave (RF-011)")
col1, col2, col3 = st.columns(3)

col1.metric("Total de Vagas Ativas", df_vagas_filtradas.shape[0])
col2.metric("Média de Habilidades por Vaga", round(df_filtrado.shape[0] / df_vagas_filtradas.shape[0], 1) if df_vagas_filtradas.shape[0] > 0 else 0)
col3.metric("Localização Mais Demandada", df_vagas_filtradas['localizacao'].mode().iloc[0] if not df_vagas_filtradas.empty else "N/A")


# --- RF-014: Gráfico de Barras - Habilidades Mais Demandadas ---
st.header("Habilidades Mais Demandadas (RF-014)")
if not df_filtrado.empty:
    top_habilidades = df_filtrado['habilidade'].value_counts().reset_index()
    top_habilidades.columns = ['Habilidade', 'Contagem']
    
    fig_habilidades = px.bar(
        top_habilidades.head(10), 
        x='Contagem', 
        y='Habilidade', 
        orientation='h',
        title='Top 10 Habilidades Técnicas',
        color='Contagem',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_habilidades.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_habilidades, use_container_width=True)
else:
    st.warning("Nenhuma vaga encontrada com os filtros aplicados para análise de habilidades.")

# --- RF-012: Mapa de Calor Geográfico (Simulado) ---
st.header("Distribuição Geográfica (RF-012 - Simulado)")
st.info("A criação de um mapa de calor geográfico real requer dados de latitude/longitude e um mapa GeoJSON do Brasil. Para este protótipo, simulamos a distribuição por localização.")

if not df_vagas_filtradas.empty:
    distribuicao_local = df_vagas_filtradas['localizacao'].value_counts().reset_index()
    distribuicao_local.columns = ['Localização', 'Contagem']
    
    fig_local = px.pie(
        distribuicao_local, 
        values='Contagem', 
        names='Localização', 
        title='Distribuição de Vagas por Localização',
        hole=.3
    )
    st.plotly_chart(fig_local, use_container_width=True)
else:
    st.warning("Nenhuma vaga encontrada com os filtros aplicados para análise de localização.")


# --- RF-015: Análise Temporal (Simulado) ---
st.header("Análise Temporal da Demanda (RF-015 - Simulado)")
st.info("A análise temporal requer dados de coleta em diferentes datas. Como o protótipo usa dados de uma única data, simulamos a tendência com dados fictícios.")

# Simulação de dados temporais
data_simulada = {
    'data': pd.to_datetime(['2025-09-01', '2025-09-08', '2025-09-15', '2025-09-22', '2025-09-29', '2025-10-06']),
    'Python': [10, 12, 15, 14, 18, 20],
    'Java': [8, 9, 7, 10, 11, 9],
    'SQL': [15, 18, 17, 20, 22, 25]
}
df_temporal = pd.DataFrame(data_simulada)

# Seleção de tecnologias para o gráfico
tecnologias_analise = st.multiselect(
    "Selecione as Tecnologias para Análise Temporal",
    options=['Python', 'Java', 'SQL'],
    default=['Python', 'SQL']
)

if tecnologias_analise:
    df_plot = df_temporal.melt(
        id_vars=['data'], 
        value_vars=tecnologias_analise, 
        var_name='Tecnologia', 
        value_name='Demanda'
    )
    
    fig_temporal = px.line(
        df_plot, 
        x='data', 
        y='Demanda', 
        color='Tecnologia',
        title='Tendência de Demanda por Tecnologia (Simulado)'
    )
    st.plotly_chart(fig_temporal, use_container_width=True)
else:
    st.warning("Selecione pelo menos uma tecnologia para a análise temporal.")

