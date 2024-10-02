import streamlit as st
from datetime import timedelta

def filtrar_jogador(dados_partida):
    '''
    Filtra os dados com base no jogador selecionado
    '''
    jogadores = dados_partida.sort_values(['player'])
    jogadores_ids = ['TODOS'] + list(jogadores['player_id'].dropna().unique())

    def get_player_name(player_id):
        if player_id == 'TODOS':
            return player_id
        p = jogadores[jogadores.player_id==player_id].iloc[0]
        return f'{p['player']} ({p['team']})'

    st.session_state['jogador_selecionado_id'] = st.sidebar.selectbox('Selecione um jogador', jogadores_ids, format_func=get_player_name)
    jogador_selecionado_id = st.session_state['jogador_selecionado_id']

    # Informações do Jogador Selecionado
    st.subheader('Jogador selecionado')
    if jogador_selecionado_id == "TODOS":
        st.write("Nenhum jogador selecionado, mostrando gráficos para todos os jogadores.")
        return dados_partida
    else:
        jogador_selecionado_data = jogadores[jogadores.player_id==jogador_selecionado_id].iloc[0]
        st.session_state['jogador_selecionado_nome'] = jogador_selecionado_data.player
        jogador_selecionado_team = jogador_selecionado_data.team
        jogador_selecionado_position  = jogador_selecionado_data.position
        st.markdown(f'**Nome**: {st.session_state['jogador_selecionado_nome']}')
        st.markdown(f'**Time**: {jogador_selecionado_team}')
        st.markdown(f'**Posição**: {jogador_selecionado_position}')
        # Filtrando os dados da partida para o jogador
        dados_partida_filtrados = dados_partida[dados_partida['player_id'] == jogador_selecionado_id]
        return dados_partida_filtrados
    
def filtrar_intervalo_tempo(dados_partida):
    '''
    Filtra os dados com base no intervalo de tempo da partida selecionado
    '''
    st.subheader('Filtro de Intervalo de Tempo da Partida')
    tempos = dados_partida.period.unique()
    for t in tempos:
        checkbox_texts = ['_', '1º Tempo', '2º Tempo', '1º Tempo da Prorrogação', '2º Tempo da Prorrogação', 'Pênaltis']
        tempo = checkbox_texts[t]
        usar_tempo = st.checkbox(tempo, value=True)
        if usar_tempo:
            dados_partida_tempo = dados_partida[dados_partida.period == t]
            min_timestamp = dados_partida_tempo.timestamp.min()
            max_timestamp = dados_partida_tempo.timestamp.max()
            timestamps = st.slider(f'Intervalo de Tempo ({tempo}):', min_value=min_timestamp, max_value=max_timestamp, value=(min_timestamp, max_timestamp), step=timedelta(minutes=1))
            dados_partida = dados_partida[(dados_partida.period != t) | ((dados_partida.period == t) & (dados_partida.timestamp >= timestamps[0]) & (dados_partida.timestamp <= timestamps[1]))]
        else:
            dados_partida = dados_partida[(dados_partida.period != t)]
    
    return dados_partida

def filtrar_eventos(dados_partida):
    '''
    Filtra os eventos da tabela final
    '''
    st.subheader('Filtrar eventos na tabela final:')

    # Número de Eventos
    total_eventos = len(dados_partida)
    if total_eventos > 1:
        st.session_state['num_eventos'] = st.slider('Número de eventos:', min_value=1, max_value=total_eventos, value=total_eventos)
        dados_partida = dados_partida.head(st.session_state['num_eventos'])
    else:
        num_eventos_text = 'não há nenhum evento' if total_eventos == 0 else 'há apenas 1 evento'
        st.text(f"Não é possível filtrar quando {num_eventos_text}.")
    
    # Exibir as informações filtradas
    st.subheader(f'Eventos a serem exportados:')
    st.dataframe(dados_partida)
        
    return dados_partida
