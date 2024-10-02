# ---------------------
# Importar bibliotecas necessárias
# ---------------------
import streamlit as st
from dados import carregar_competicao_temporada_partida
from metricas import metricas_eventos_partida
from filtros import filtrar_jogador, filtrar_intervalo_tempo, filtrar_eventos
from visualizacoes import carregar_visualizacoes
from exportar import download_csv

# ---------------------
# Títulos do Dashboard
# ---------------------
st.title("Análise Interativa de Partidas ⚽")
st.sidebar.header("Configurações")

# ---------------------
# Obter eventos da partida, exibir métricas e eventos
# ---------------------

# Obter eventos da partida a partir de seletores de competição, temporada e partida
partida_selecionada, dados_partida = carregar_competicao_temporada_partida()

# Mostrar métricas e eventos da partida
metricas_eventos_partida(partida_selecionada, dados_partida)

# ---------------------
# Filtrar dados da partida
# ---------------------

# Filtro de Jogador
dados_partida = filtrar_jogador(dados_partida)

# Filtro de Intervalo de Tempo da Partida
dados_partida = filtrar_intervalo_tempo(dados_partida)

# ---------------------
# Visualizações de dados
# ---------------------

# Carregar visualizações de dados da partida
carregar_visualizacoes(dados_partida)

# ---------------------
# Filtro de eventos e download do CSV
# ---------------------

# Filtra e exibe os eventos da tabela final
dados_partida = filtrar_eventos(dados_partida)

# Exibe opção para download do csv
download_csv(dados_partida, partida_selecionada)
