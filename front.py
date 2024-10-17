import streamlit as st  # Streamlit é utilizado para criar interfaces web 
import pandas as pd  
import requests  # Requests é utilizado para fazer requisições HTTP (GET, POST, etc.)

# Base URL da API do backend (Flask)
BASE_URL = "http://127.0.0.1:5000"

# Função genérica para fazer requisições ao backend
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    url = f"{BASE_URL}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        else:
            st.error("Método HTTP não suportado.")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")

        return None
    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        return None

# Inicializa o session_state para controlar qual formulário exibir
if 'mostrar_cadastro_usuario' not in st.session_state:
    st.session_state.mostrar_cadastro_usuario = False

if 'mostrar_cadastro_bike' not in st.session_state:
    st.session_state.mostrar_cadastro_bike = False

# Função de cadastro de usuário
def cadastrar_usuario():
    st.write("### Cadastro de Usuário")
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    data_nascimento = st.text_input("Data de Nascimento (AAAA-MM-DD)")

    if st.button("Cadastrar Usuário"):
        if nome and cpf and data_nascimento:
            data = {
                'nome': nome.strip(),
                'cpf': cpf.strip(),
                'data_nascimento': data_nascimento.strip()
            }
            response = fazer_requisicao("usuarios", method="POST", data=data)
            if response:
                st.success("✅ Usuário cadastrado com sucesso!")
            else:
                st.error("⚠️ Erro ao cadastrar o usuário.")
        else:
            st.error("⚠️ Todos os campos são obrigatórios.")

# Função de cadastro de bicicleta
def cadastrar_bike():
    st.write("### Cadastro de Bicicleta")
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    cidade = st.text_input("Cidade")
    status = st.selectbox("Status", ["", "livre", "em uso"])

    if st.button("Cadastrar Bicicleta"):
        if marca and modelo and cidade and status:
            data = {
                'marca': marca.strip(),
                'modelo': modelo.strip(),
                'cidade': cidade.strip(),
                'status': status.strip()
            }
            response = fazer_requisicao("bikes", method="POST", data=data)
            if response:
                st.success("✅ Bicicleta cadastrada com sucesso!")
            else:
                st.error("⚠️ Erro ao cadastrar a bicicleta.")
        else:
            st.error("⚠️ Todos os campos são obrigatórios.")

# Botões na barra lateral para escolher o que exibir
st.sidebar.write("### Ações de Cadastro:")
if st.sidebar.button("Cadastrar Usuário"):
    st.session_state.mostrar_cadastro_usuario = True
    st.session_state.mostrar_cadastro_bike = False

if st.sidebar.button("Cadastrar Bicicleta"):
    st.session_state.mostrar_cadastro_bike = True
    st.session_state.mostrar_cadastro_usuario = False

# Filtros de busca (esses ficam sempre visíveis)
st.sidebar.header("🔍 Filtros de Pesquisa")
marca = st.sidebar.text_input("📍 Digite a marca") 
modelo = st.sidebar.text_input("📍 Digite o modelo") 
cidade = st.sidebar.text_input("📍 Digite a cidade") 
status = st.sidebar.selectbox("📍 Digite o status", ["", "livre", "em uso"])

# Função para buscar bicicletas
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

# Botão para buscar bikes (esse também fica sempre visível)
if st.sidebar.button("🔍 Buscar bikes"):
    buscar_bikes()

# Título principal
st.title("Alugue sua bike aqui")
st.write("---")

# Exibe o formulário de cadastro de usuário ou bicicleta dependendo do botão clicado
if st.session_state.mostrar_cadastro_usuario:
    cadastrar_usuario()

if st.session_state.mostrar_cadastro_bike:
    cadastrar_bike()
