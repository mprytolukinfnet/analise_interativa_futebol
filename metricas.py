import streamlit as st
import plotly.express as px


# Função para selecionar a cor da métrica da partida de acordo com parâmetros
def select_color(n, min_n, max_n):
    # n == métrica
    # min_n == valor mínimo esperado
    # max_n == valor máximo esperado
    colors = px.colors.sequential.Oranges
    color_position = max(min(int(8 * (n - min_n) / (max_n - min_n)), 8), 0)
    return colors[color_position]


@st.cache_data
def metricas_eventos_partida(partida_selecionada, dados_partida):
    # Exibir informações básicas
    st.subheader(
        f"{partida_selecionada.home_team} ({partida_selecionada.home_score}) x {partida_selecionada.away_team} ({partida_selecionada.away_score})"
    )
    st.write(f"**Competição:** {st.session_state['competicao_nome']}")
    st.write(f"**Temporada:** {st.session_state['temporada_ano']}")
    st.write(f"**Data:** {partida_selecionada.match_date}")
    num_gols_partida = partida_selecionada.home_score + partida_selecionada.away_score
    num_chutes_partida = len(dados_partida[dados_partida.type == "Shot"])
    num_passes_partida = len(dados_partida[dados_partida.type == "Pass"])

    # Aplicar cores às métricas de acordo com o valor
    cores_metricas = f"""
    <style>
    .e1f1d6gn3:nth-of-type(1) > div > div > div > div > div > div {{
    color: {select_color(num_gols_partida, 0, 10)};
    }}

    .e1f1d6gn3:nth-of-type(2) > div > div > div > div > div > div {{
    color: {select_color(num_chutes_partida, 10, 50)};
    }}

    .e1f1d6gn3:nth-of-type(3) > div > div > div > div > div > div {{
    color: {select_color(num_passes_partida, 1000, 1500)};
    }}

    </style>
    """
    st.markdown(cores_metricas, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("**Gols**", num_gols_partida)
    with col2:
        st.metric("**Chutes:**", num_chutes_partida)
    with col3:
        st.metric("**Passes:**", num_passes_partida)

    # Mostrar um DataFrame com os eventos da partida
    st.write("Eventos da Partida:")
    st.dataframe(dados_partida)
