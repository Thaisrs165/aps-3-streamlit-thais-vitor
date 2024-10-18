import streamlit as st
import pandas as pd
import requests
BASE_URL = "http://127.0.0.1:5000"

def requisicao(endpoint, method="GET", data=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"} 

    try:
        response = requests.request(method, url, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
        else:
            st.error(f"⚠️ Erro {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
    return None

def load_data():
    users = requisicao("usuarios")
    bikes = requisicao("bikes", method="GET", data={"status": "livre"})

    if users is not None:
        df_usuarios = pd.DataFrame(users['lista'])
    else:
        df_usuarios = pd.DataFrame()

    if bikes is not None:
        df_bikes = pd.DataFrame(bikes['lista'])
    else:
        df_bikes = pd.DataFrame()

    return df_usuarios, df_bikes

st.title("🚲 Sistema de Empréstimos de Bikes")

df_usuarios, df_bikes = load_data()

if not df_usuarios.empty and not df_bikes.empty:
    st.write("### 👥 Usuários Disponíveis")
    st.dataframe(df_usuarios[['nome', 'cpf']])

    st.write("### 🚲 Bikes Disponíveis")
    st.dataframe(df_bikes[['marca', 'modelo', 'cidade']])

    usuarios_opc = list(df_usuarios['nome'])
    usuario_select = st.selectbox("Selecione o Usuário", usuarios_opc)
    id_usuario = df_usuarios.loc[df_usuarios['nome'] == usuario_select, '_id'].values[0]

    bikes_opc = list(df_bikes['marca'] + " " + df_bikes['modelo'])
    bike_select = st.selectbox("Selecione a Bike", bikes_opc)
    bike_index = bikes_opc.index(bike_select)
    id_bike = df_bikes.iloc[bike_index]['_id']

    if st.button("📥 Confirmar Empréstimo"):
        emprestimo = requisicao(
            f"emprestimos/usuarios/{id_usuario}/bikes/{id_bike}", 
            method="POST", 
            data={}
        )
        if emprestimo:
            st.success("🚲 Empréstimo registrado com sucesso!")
else:
    st.error("⚠️ Não há dados suficientes para realizar um empréstimo.")

