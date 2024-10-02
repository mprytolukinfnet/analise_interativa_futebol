import streamlit as st
import pandas as pd
from statsbombpy import sb
# ---------------------
# Funções para carregar dados
# ---------------------
# Carrega os dados de competições
@st.cache_data
def carregar_competicoes():
    return sb.competitions()

# Carrega as partidas de uma temporada de uma competição
@st.cache_data
def carregar_partidas(competicao_id, season_id):
    return sb.matches(competition_id=competicao_id, season_id = season_id)

# Carrega os eventos de uma partida
@st.cache_data
def carregar_eventos_partida(jogo_id):
    eventos_partida = sb.events(match_id=jogo_id)
    eventos_partida['timestamp'] = pd.to_datetime(eventos_partida['timestamp'], format='%H:%M:%S.%f').dt.time 
    return eventos_partida

# ---------------------
# Função para selecionar/carregar dados
# ---------------------

def carregar_competicao_temporada_partida():
    '''
    Seleciona a Competição, a Temporada e a Partida com base na opção do usuário
    Retorna:
        (partida_selecionada, dados_partida, temporada_ano)
        (Pandas.Series, Pandas.DateTime, string)
    '''
    progresso = st.progress(0)
    with st.spinner('Carregando dados...'):
        # Seletor de competição
        competicoes = carregar_competicoes()
        st.session_state['competicao_nome'] = st.sidebar.selectbox('Selecione uma competição', competicoes['competition_name'].unique())
        competicao = competicoes[competicoes['competition_name'] == st.session_state['competicao_nome']].iloc[0]
        
        progresso.progress(33)

        # Seletor de temporada
        temporadas = competicoes[competicoes['competition_id'] == competicao['competition_id']]
        st.session_state['temporada_ano'] = st.sidebar.selectbox('Selecione uma temporada', temporadas['season_name'].unique())
        temporada = temporadas[temporadas['season_name'] == st.session_state['temporada_ano']].iloc[0]

        progresso.progress(66)

        # Seletor de partida
        partidas = carregar_partidas(competicao['competition_id'], temporada['season_id']).sort_values(['home_team', 'away_team', 'match_date'])
        def get_match_title(match_id):
            p = partidas[partidas.match_id==match_id].iloc[0]
            return f'{p['home_team']} x {p['away_team']} ({p['match_date']})'
        partida_id = st.sidebar.selectbox('Selecione uma partida', partidas['match_id'].unique(), format_func=get_match_title)
        partida_selecionada = partidas[partidas.match_id==partida_id].iloc[0]

        # Carregar os dados da partida selecionada
        dados_partida = carregar_eventos_partida(partida_id)

        progresso.progress(100)
    
    progresso.empty()

    return partida_selecionada, dados_partida
