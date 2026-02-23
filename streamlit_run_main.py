import streamlit as st
import sqlite3
from datetime import datetime
import time

# --- CONFIGURAÇÃO DO BANCO DE DATOS ---
def init_db():
    conn = sqlite3.connect('racao_segura_v010.db')
    c = conn.cursor()
    # Tabela principal para todos os cadastros citados
    c.execute('''CREATE TABLE IF NOT EXISTS cadastros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_registro TEXT,
                    detalhes TEXT,
                    valor_qtd REAL,
                    data_fab TEXT,
                    data_val TEXT,
                    timestamp DATETIME)''')
    conn.commit()
    conn.close()

def salvar_dados(tipo, detalhes, valor=0, fab="", val=""):
    conn = sqlite3.connect('racao_segura_v010.db')
    c = conn.cursor()
    c.execute("INSERT INTO cadastros (tipo_registro, detalhes, valor_qtd, data_fab, data_val, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (tipo, detalhes, valor, fab, val, datetime.now()))
    conn.commit()
    conn.close()

# --- INICIALIZAÇÃO DO ESTADO DO SISTEMA ---
if 'sistema_ativo' not in st.session_state:
    st.session_state.sistema_ativo = True

init_db()

# --- LÓGICA DO LOOP DE INTERFACE ---
if not st.session_state.sistema_ativo:
    st.error("⚠️ O SISTEMA DA FÁBRICA FOI DESLIGADO.")
    if st.button("Religar Sistema"):
        st.session_state.sistema_ativo = True
        st.rerun()
    st.stop() # Interrompe o loop do Streamlit aqui

# --- INTERFACE ---
st.title("🛡️ Ração Segura v0.1.0")
st.sidebar.header("Painel de Operações")

# Opções de Cadastro conforme sua solicitação
categoria = st.sidebar.selectbox("Selecione a Operação", [
    "Produto e Animal", "Análise Laboratorial", "Fornecedor", 
    "Produção Diária/Mensal", "Estoque", "Vendas e Pedidos", "Perdas"
])

st.subheader(f"Cadastro de {categoria}")

with st.form("form_geral", clear_on_submit=True):
    if categoria == "Produto e Animal":
        nome = st.text_input("Nome da Ração")
        tipo_animal = st.text_input("Tipo de Animal (ex: Bovino)")
        peso = st.number_input("Peso (kg)", min_value=0.0)
        fab = st.date_input("Data de Fabricação")
        val = st.date_input("Data de Validade")
        detalhes = f"Ração: {nome} | Animal: {tipo_animal}"
        
    elif categoria == "Produção Diária/Mensal":
        periodo = st.radio("Período", ["Diária", "Mensal"])
        qtd = st.number_input("Quantidade Produzida (kg)")
        detalhes = f"Produção {periodo}"
        
    elif categoria == "Vendas e Pedidos":
        tipo = st.radio("Tipo", ["Venda", "Pedido"])
        valor = st.number_input("Valor total (R$)")
        detalhes = f"Registro de {tipo}"

    # Adicione os outros campos conforme necessário seguindo o padrão...

    enviar = st.form_submit_button("Confirmar Registro")

    if enviar:
        # Aqui a lógica salva no SQLite e o loop continua
        salvar_dados(categoria, detalhes, valor=locals().get('peso', 0) or locals().get('qtd', 0) or locals().get('valor', 0))
        st.success(f"✅ {categoria} registrado no SQLite!")

# --- BOTÃO DE DESLIGAMENTO ---
st.sidebar.markdown("---")
if st.sidebar.button("🔴 DESLIGAR SISTEMA NA FÁBRICA"):
    st.session_state.sistema_ativo = False
    st.rerun()

# Visualização em Tempo Real (Opcional)
if st.checkbox("Mostrar últimos registros do banco"):
    conn = sqlite3.connect('racao_segura_v010.db')
    data = conn.execute("SELECT * FROM cadastros ORDER BY id DESC LIMIT 10").fetchall()
    st.table(data)
    conn.close()
