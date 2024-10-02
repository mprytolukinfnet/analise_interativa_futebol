import streamlit as st

def download_csv(dados_partida, partida_selecionada):
    # Botão de download dos dados filtrados
    st.sidebar.markdown("### Baixar eventos filtrados")

    csv_data = dados_partida.to_csv(index=False)
    csv_file_name = f'{partida_selecionada.home_team}_x_{partida_selecionada.away_team}_({partida_selecionada.match_date})'

    if st.session_state['jogador_selecionado_id'] != "TODOS":
        csv_file_name += f'_{st.session_state['jogador_selecionado_nome']}'

    csv_file_name = csv_file_name.replace(' ','_')

    st.sidebar.download_button(label="Baixar CSV", data=csv_data, file_name=f'{csv_file_name}.csv', mime='text/csv')
