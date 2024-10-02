import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch, PyPizza
import seaborn as sns
import numpy as np


@st.cache_data
def get_passes(dados_partida):
    # Filtrar os eventos de passe
    return dados_partida[dados_partida["type"] == "Pass"]


@st.cache_data
def get_chutes(dados_partida):
    # Filtrar os eventos de chute
    return dados_partida[dados_partida["type"] == "Shot"]


@st.cache_data
def mapa_de_passes(dados_partida):
    passes = get_passes(dados_partida)
    st.subheader("Mapa de Passes")
    # Criar o campo para o mapa de passes
    pitch = Pitch(line_color="black", pitch_type="statsbomb")
    fig, ax = plt.subplots(figsize=(10, 6))
    pitch.draw(ax=ax)

    # Adicionar os passes ao campo
    for _, passe in passes.iterrows():
        pitch.arrows(
            passe["location"][0],
            passe["location"][1],
            passe["pass_end_location"][0],
            passe["pass_end_location"][1],
            ax=ax,
            color="blue",
            width=2,
            headwidth=3,
            alpha=0.6,
        )

    # Exibir o mapa de passes no Streamlit
    st.pyplot(fig)


@st.cache_data
def mapa_de_chutes(dados_partida):
    chutes = get_chutes(dados_partida)
    st.subheader("Mapa de Chutes")
    # Criar o campo para o mapa de chutes
    pitch = Pitch(line_color="black", pitch_type="statsbomb")
    fig, ax = plt.subplots(figsize=(10, 6))
    pitch.draw(ax=ax)

    # Adicionar os chutes ao campo (com distinção entre gol e chute perdido)
    for _, chute in chutes.iterrows():
        color = "green" if chute["shot_outcome"] == "Goal" else "red"
        pitch.scatter(
            chute["location"][0],
            chute["location"][1],
            ax=ax,
            color=color,
            s=100,
            edgecolor="black",
            alpha=0.8,
        )

    # Exibir o mapa de chutes no Streamlit
    st.pyplot(fig)


@st.cache_data
def passes_e_gols(dados_partida):
    passes = get_passes(dados_partida)
    chutes = get_chutes(dados_partida)
    # Relação entre passes e gols
    st.subheader("Proporção de Passes e Gols")
    gols = len(chutes[chutes["shot_outcome"] == "Goal"])
    passes_total = len(passes)

    # Gráfico de pizza para mostrar a proporção de passes para gols

    # Dados para o gráfico de pizza
    sizes = [passes_total - gols, gols]
    labels = ["Total de Passes", "Gols"]
    colors = ["#3498db", "#2ecc71"]

    if passes_total == 0 and gols == 0 or gols > passes_total:
        st.text("Não é possível exibir o gráfico.")
    else:
        # Criando o gráfico de pizza
        fig, ax = plt.subplots()
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": "black"},
        )
        ax.axis("equal")  # Assegura que o gráfico seja um círculo

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)


@st.cache_data
def distancia_probabilidade_e_resultado_chutes(dados_partida):
    chutes = get_chutes(dados_partida)
    # Usando Seaborn para criar um gráfico de dispersão que mostra a relação entre distância, probabilidade de gol e resultado
    st.subheader("Relação entre Distância, Probabilidade de Gol e Resultado dos Chutes")

    # Filtrar chutes com dados válidos de distância e probabilidade de gol
    chutes_validos = chutes.dropna(subset=["shot_statsbomb_xg", "location"])
    chutes_validos["distancia"] = chutes_validos["location"].apply(
        lambda x: x[0]
    )  # Usando o primeiro valor da posição como distância

    # Criando gráfico de dispersão
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        x="distancia",
        y="shot_statsbomb_xg",
        data=chutes_validos,
        ax=ax,
        hue="shot_outcome",
        palette="coolwarm",
    )

    ax.set_title("Distância vs. Probabilidade de Gol (xG)")
    ax.set_xlabel("Distância (em metros)")
    ax.set_ylabel("Probabilidade de Gol (xG)")

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


@st.cache_data
def pizza_percentuais(dados_partida):
    # Percentuais de acerto de um jogador individual ou da partida
    st.subheader("Percentuais de Acerto")
    # Definir as categorias e valores
    dribles_counts = dados_partida[
        dados_partida.type == "Dribble"
    ].dribble_outcome.value_counts(dropna=False)
    dribles_perc = (
        round(dribles_counts.get("Complete", 0) / dribles_counts.sum() * 100, 1)
        if len(dribles_counts) > 0
        else np.nan
    )

    passes_counts = dados_partida[
        (dados_partida.type == "Pass") & (dados_partida.pass_outcome != "Unknown")
    ].pass_outcome.value_counts(dropna=False)
    passes_perc = (
        round(passes_counts[np.nan] / passes_counts.sum() * 100, 1)
        if len(passes_counts) > 0
        else np.nan
    )

    final_counts = dados_partida[
        dados_partida.type == "Shot"
    ].shot_outcome.value_counts(dropna=False)
    final_perc = (
        round(
            (final_counts.get("Saved", 0) + final_counts.get("Goal", 0))
            / final_counts.sum()
            * 100,
            1,
        )
        if len(final_counts) > 0
        else np.nan
    )

    recepcoes_counts = dados_partida[
        dados_partida.type == "Ball Receipt*"
    ].ball_receipt_outcome.value_counts(dropna=False)
    recepcoes_perc = (
        round(recepcoes_counts[np.nan] / recepcoes_counts.sum() * 100, 1)
        if len(recepcoes_counts) > 0
        else np.nan
    )

    intercept_counts = dados_partida[
        dados_partida.type == "Interception"
    ].interception_outcome.value_counts(dropna=False)
    intercept_perc = (
        round(intercept_counts.get("Won", 0) / intercept_counts.sum() * 100, 1)
        if len(intercept_counts) > 0
        else np.nan
    )

    params = [
        "Dribles-Sucesso (%)",
        "Passes-Sucesso (%)",
        "Finalizações a Gol (%)",
        "Recepções-Sucesso (%)",
        "Interceptações-Sucesso (%)",
    ]
    values = [dribles_perc, passes_perc, final_perc, recepcoes_perc, intercept_perc]

    stats = {
        "Dribles-Sucesso (%)": dribles_perc,
        "Passes-Sucesso (%)": passes_perc,
        "Finalizações a Gol (%)": final_perc,
        "Recepções-Sucesso (%)": recepcoes_perc,
        "Interceptações-Sucesso (%)": intercept_perc,
    }

    # Dicionário com estatísticas que não são nulas para um jogador/partida
    non_null_stats = {k: v for k, v in stats.items() if not np.isnan(v)}

    params = non_null_stats.keys()
    values = list(non_null_stats.values())
    n_params = len(params)

    # Se tiver mais de um parâmetro não-nulo, gera o gráfico
    if n_params > 0:
        # Criação do gráfico pizza
        baker = PyPizza(
            params=params,
            background_color="#222222",
            straight_line_color="#000000",
            straight_line_lw=1,
            last_circle_color="#000000",
            last_circle_lw=1,
            other_circle_lw=0,
            other_circle_color="#000000",
        )

        fig, ax = baker.make_pizza(
            values,
            figsize=(8, 8),
            color_blank_space="same",
            slice_colors=["#1f77b4"] * n_params,
            value_colors=["#FFFFFF"] * n_params,
            value_bck_colors=["#1f77b4"] * n_params,
            kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=2),
            kwargs_params=dict(color="#FFFFFF", fontsize=12),
            kwargs_values=dict(
                color="#FFFFFF",
                fontsize=11,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000",
                    facecolor="#1f77b4",
                    boxstyle="round,pad=0.3",
                    lw=2,
                ),
            ),
        )

        # Exibir o gráfico Pizza Plot no Streamlit
        st.pyplot(fig)
    else:
        st.text("Não é possível exibir o gráfico.")


def carregar_visualizacoes(dados_partida):
    progresso = st.progress(0)
    with st.spinner("Carregando visualizações..."):
        # Mapa de Passes
        mapa_de_passes(dados_partida)
        progresso.progress(20)

        # Mapa de Chutes
        mapa_de_chutes(dados_partida)
        progresso.progress(40)

        # Proporção de Passes e Gols
        passes_e_gols(dados_partida)
        progresso.progress(60)

        # Relação entre Distância, Probabilidade de Gol e Resultado dos Chutes
        distancia_probabilidade_e_resultado_chutes(dados_partida)
        progresso.progress(80)

        # Gráfico de "Pizza Plot" dos percentuais de acerto de um jogador (ou todos)
        pizza_percentuais(dados_partida)
        progresso.progress(100)
    progresso.empty()
