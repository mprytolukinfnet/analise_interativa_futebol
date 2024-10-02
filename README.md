# Análise Interativa de Partidas de Futebol ⚽

Este projeto é um dashboard interativo desenvolvido com [Streamlit](https://streamlit.io/), que utiliza dados de partidas de futebol fornecidos pela [StatsBomb](https://statsbomb.com/) para análise detalhada de eventos, métricas e visualizações das partidas. O usuário pode selecionar uma competição, temporada e partida específicas e aplicar diversos filtros para explorar os dados.

O projeto está disponível na Streamlit Community Cloud em: https://mprytoluk-dashboard-interativo-futebol.streamlit.app/

## Estrutura do Projeto

- **app.py**: O arquivo principal da aplicação Streamlit, responsável pela interação com o usuário e exibição das visualizações e métricas.
- **dados.py**: Contém funções para carregar os dados de competições, temporadas, partidas e eventos, utilizando a API da StatsBomb.
- **exportar.py**: Gerencia a exportação dos dados filtrados em formato CSV para download.
- **filtros.py**: Define funções que permitem filtrar os dados com base em jogador, intervalo de tempo da partida e eventos específicos.
- **metricas.py**: Exibe as principais métricas e estatísticas da partida selecionada.
- **visualizacoes.py**: Responsável por gerar visualizações gráficas, como mapas de passes e chutes, gráficos de pizza, entre outros.
- **requirements.txt**: Lista as dependências necessárias para rodar o projeto.

## Funcionalidades

1. **Seleção de Competição, Temporada e Partida**: O usuário pode escolher a competição e temporada de interesse, e a partir disso, selecionar uma partida para análise.
2. **Métricas da Partida**: Exibição de estatísticas como número de gols, chutes e passes.
3. **Filtros**:
   - **Jogador**: Filtra os eventos da partida com base no jogador selecionado.
   - **Intervalo de Tempo**: Permite a seleção de períodos específicos da partida (1º tempo, 2º tempo, prorrogações, etc.).
   - **Eventos**: Filtra e exibe eventos específicos para visualização.
4. **Visualizações**:
   - **Mapa de Passes**: Mostra os passes realizados na partida.
   - **Mapa de Chutes**: Visualiza os chutes ao gol, distinguindo entre chutes convertidos em gol e os que não foram.
   - **Proporção de Passes e Gols**: Gráfico de pizza mostrando a relação entre passes e gols.
   - **Distância, Probabilidade e Resultado dos Chutes**: Gráfico de dispersão exibindo a relação entre distância do chute, probabilidade de gol (xG) e o resultado.
5. **Exportação de Dados**: Permite o download dos eventos filtrados da partida em formato CSV.

## Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/mprytolukinfnet/analise_interativa_futebol.git
   cd analise-partidas

2. Criar um Ambiente Virtual

No diretório do projeto, crie um ambiente virtual usando `virtualenv`:

```bash
virtualenv venv
```

3. Ativar o Ambiente Virtual
- No Windows:
```bash
venv\Scripts\activate
```

- No Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

5. Executar o Dashboard
Para rodar a aplicação, execute o seguinte comando no terminal:
```bash
streamlit run app.py
```

A aplicação estará disponível no seu navegador, normalmente acessível no endereço http://localhost:8501.