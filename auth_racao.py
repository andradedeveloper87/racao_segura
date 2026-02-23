import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import re
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('racao_segura.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registros 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, detalhes TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- CONFIGURAÇÃO DE AUTENTICAÇÃO ---
# Em um sistema real, essas senhas devem vir de um banco de dados ou arquivo YAML
# Aqui as senhas já devem estar em HASH para segurança.
names = ['Operador Fábrica', 'Gerente']
usernames = ['operador1', 'gerente1']
passwords = ['senha_em_hash_1', 'senha_em_hash_2'] # Use stauth.Hasher para gerar

authenticator = stauth.Authenticate(
    {'usernames': {
        usernames[0]: {'name': names[0], 'password': passwords[0]},
        usernames[1]: {'name': names[1], 'password': passwords[1]}
    }},
    'racao_segura_cookie', 'auth_key', cookie_expiry_days=1
)

# --- LÓGICA DE VALIDAÇÃO DE SENHA (REQUISITO: 10 letras, 2 números, 1 especial) ---
def validar_complexidade(senha):
    letras = len(re.findall(r'[a-zA-Z]', senha))
    numeros = len(re.findall(r'[0-9]', senha))
    especiais = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', senha))
    return letras >= 10 and numeros >= 2 and especiais >= 1

# --- INTERFACE DE LOGIN ---
name, authentication_status, username = authenticator.login('Login - Ração Segura v0.1.0', 'main')

if authentication_status == False:
    st.error('Usuário/Senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, insira usuário e senha')
elif authentication_status:

    # --- INICIALIZAÇÃO DO LOOP DE OPERAÇÃO ---
    if 'sistema_ativo' not in st.session_state:
        st.session_state.sistema_ativo = True

    # VERIFICAÇÃO DO BOTÃO DE DESLIGAMENTO (PARA O LOOP)
    if not st.session_state.sistema_ativo:
        st.error("🔴 SISTEMA ENCERRADO NA FÁBRICA. OPERAÇÕES SUSPENSAS.")
        if st.button("Reiniciar Sistema"):
            st.session_state.sistema_ativo = True
            st.rerun()
        st.stop()

    # --- INTERFACE DO SISTEMA ATIVO ---
    st.sidebar.title(f"Bem-vindo, {name}")
    authenticator.logout('Sair do Sistema', 'sidebar')
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚨 DESLIGAR FÁBRICA"):
        st.session_state.sistema_ativo = False
        st.rerun()

    menu = st.sidebar.selectbox("Operação", [
        "Cadastro de Produto", "Análise de Qualidade", "Produção Diária", "Vendas/Pedidos"
    ])

    st.header(f"Setor: {menu}")

    # Exemplo de formulário de Loop Infinito (Input -> SQLite -> Repeat)
    with st.form("registro_fabrica", clear_on_submit=True):
        if menu == "Cadastro de Produto":
            prod = st.text_input("Nome da Ração")
            animal = st.text_input("Tipo de Animal")
            if st.form_submit_button("Registrar no SQLite"):
                conn = sqlite3.connect('racao_segura.db')
                conn.execute("INSERT INTO registros (categoria, detalhes, timestamp) VALUES (?, ?, ?)",
                             (menu, f"{prod} para {animal}", datetime.now()))
                conn.commit()
                conn.close()
                st.success("Dados enviados ao banco com sucesso!")

    # Exibição dos dados salvos no loop atual
    if st.checkbox("Ver monitoramento em tempo real"):
        conn = sqlite3.connect('racao_segura.db')
        df = conn.execute("SELECT * FROM registros ORDER BY id DESC").fetchall()
        st.write(df)
        conn.close()
