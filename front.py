import streamlit as st  # Streamlit é utilizado para criar interfaces web 
import pandas as pd  
import requests  # Requests é utilizado para fazer requisições HTTP (GET, POST, etc.)

# Base URL da API do backend (Flask)
BASE_URL = "http://127.0.0.1:5000" 
# Definimos a base URL onde o backend está rodando (localmente no endereço 127.0.0.1 na porta 5000).
# Todas as requisições da aplicação serão enviadas para esse endpoint (ou serviço), concatenando o recurso desejado.

# Função genérica para fazer requisições ao backend
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    # Constrói a URL completa concatenando o endpoint específico com a base URL
    url = f"{BASE_URL}/{endpoint}"

    # Monta a requisição de acordo com o método HTTP fornecido
    try:
        if method == "GET":
            response = requests.get(url, params=params)
            # Método GET: Envia os parâmetros da requisição (params) como query strings na URL.
            # Exemplo: /imoveis?tipo_imovel=Casa&preco_min=200000&preco_max=1000000

        elif method == "POST":
            response = requests.post(url, json=data)
            # Método POST: Envia os dados no corpo da requisição em formato JSON para criar novos recursos no backend.
            # Exemplo: POST /imoveis para criar um novo imóvel, enviando os detalhes no corpo da requisição.

        elif method == "PUT":
            response = requests.put(url, json=data)
            # Método PUT: Envia os dados no corpo da requisição em formato JSON para atualizar um recurso existente.

        elif method == "DELETE":
            response = requests.delete(url, params=params)
            # Método DELETE: Envia parâmetros na URL para deletar um recurso específico no backend.

        else:
            st.error("Método HTTP não suportado.")
            # Caso um método HTTP não suportado seja passado, exibe um erro no frontend do Streamlit.

        # Verifica o status HTTP da resposta
        if response.status_code == 200:
            return response.json()  # Resposta 200 (OK): Retorna o corpo da resposta como um JSON (dicionário Python).
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
            # Se o status for 404 (Not Found), exibe um aviso de que o recurso não foi encontrado.
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
            # Se o status for 500 (Internal Server Error), exibe um erro genérico de servidor.
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")
            # Para outros códigos de status, exibe um erro genérico mostrando o código e a mensagem da resposta.

        return None  # Se não houver sucesso, retorna None para indicar falha.

    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        # Captura e exibe exceções, como erros de conexão ou outros problemas ao tentar fazer a requisição.
        return None

# Título e subtítulo da interface do aplicativo Streamlit
st.title("Alugue sua bike aqui")
# st.subheader("Encontre o imóvel perfeito para você!!!")



# Filtros na barra lateral
st.sidebar.header("🔍 Filtros de Pesquisa")

# Tipo de Imóvel - Filtro (menu suspenso)
# Marca = st.sidebar.selectbox(
#     "Marca",
#     ["Apartamento", "Casa", "Terreno", "Kitnet", "Sítio"]
# )

# Modelo = st.sidebar.selectbox(
#     "Modelo",
#     ["Apartamento", "Casa", "Terreno", "Kitnet", "Sítio"]
# )

# Cidade = st.sidebar.selectbox(
#     "Cidade",
#     ["Apartamento", "Casa", "Terreno", "Kitnet", "Sítio"]
# )

# Status = st.sidebar.selectbox(
#     "Status",
#     ["em uso", "Casa", "Terreno", "Kitnet", "Sítio"]
# )

marca = st.sidebar.text_input("📍 Digite o marca") 
modelo = st.sidebar.text_input("📍 Digite o modelo") 
cidade = st.sidebar.text_input("📍 Digite o cidade") 
status = st.sidebar.selectbox("📍 Digite o status", ["", "livre", "em uso"])

# preco_min, preco_max = st.sidebar.slider(
#     "💰 Faixa de Preço (R$)",
#     min_value=100000,
#     max_value=3000000,
#     value=(200000, 1000000),
#     step=50000
# )


# Função para buscar imóveis
# def buscar_bikes():
#     # Parâmetros para a requisição GET
#     params = {
#         'modelo': modelo,  # Inclui o tipo de imóvel selecionado pelo usuário.
#         'marca': marca,      # Inclui o valor mínimo da faixa de preço selecionada.
#         'cidade': cidade      # Inclui o valor máximo da faixa de preço selecionada.
#         # 'cep': cep if cep else None  # Inclui o CEP se for fornecido, caso contrário, deixa como None.
#     }

#     # Fazendo a requisição GET para o backend
#     data = fazer_requisicao("bikes", method="GET", params=params)
#     # Chama a função 'fazer_requisicao' para enviar uma requisição GET ao endpoint '/imoveis' do backend,
#     # com os parâmetros (filtros) fornecidos pelo usuário.

#     # Se houver dados na resposta, exibir os imóveis
#     if data and data['resultados']['quantidade'] > 0:
#         # Se a resposta contiver resultados (quantidade de imóveis for maior que 0), exibe os imóveis encontrados.
#         df_bikes = pd.DataFrame(data['resultados']['bikes'])
#         # Converte os imóveis em um DataFrame do Pandas para exibição em tabela.
#         st.write("### 🏠 Resultados da Pesquisa")
#         st.dataframe(df_bikes) 
#         # Exibe os resultados da pesquisa em uma tabela interativa no frontend do Streamlit.
#     elif data:
#         st.write("❌ Nenhuma bike encontrada para os filtros selecionados.")
#         # Se não houver resultados (mas houver dados válidos na resposta), exibe uma mensagem dizendo que 
#         # nenhum imóvel foi encontrado.


def buscar_bikes():
    params = {}
    if marca:
        params['marca'] = marca.strip()
    if modelo:
        params['modelo'] = modelo.strip()
    if cidade:
        params['cidade'] = cidade.strip()
    if status:
        params['status'] = status.strip()

    data = fazer_requisicao("bikes", method="GET", params=params)

    if data and len(data['lista']) > 0:
        st.write("### 🚲 Bikes disponíveis")
        df_bikes = pd.DataFrame(data['lista'])
        st.dataframe(df_bikes) 
    elif data:
        st.write("❌ Nenhuma bike encontrada para os filtros selecionados.")
    else:
        st.error("⚠️ Erro ao buscar bikes.")



# Botão para buscar imóveis
if st.sidebar.button("🔍 Buscar bikes"):
    buscar_bikes()


    # Quando o botão "Buscar Imóveis" é clicado, chama a função 'buscar_imoveis' para iniciar a requisição.


