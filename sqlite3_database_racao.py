import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO E BANCO DE DADOS ---
DB_NAME = "racao_segura.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabela unificada para simplificar a v0.1.0 (ou você pode criar múltiplas)
    c.execute('''CREATE TABLE IF NOT EXISTS registros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT,
                    detalhes TEXT,
                    quantidade REAL,
                    data_registro TIMESTAMP)''')
    
    # Tabela específica para Produtos/Validade
    c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    tipo_animal TEXT,
                    peso REAL,
                    fabricacao DATE,
                    validade DATE)''')
    conn.commit()
    conn.close()

def salvar_no_db(tabela, dados):
    conn = sqlite3.connect(DB_NAME)
    df = pd.DataFrame([dados])
    df.to_sql(tabela, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

# Inicializar Banco
init_db()

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Ração Segura v0.1.0", layout="centered")

st.title("🏭 Sistema Ração Segura")
st.sidebar.header("Painel de Controle")

# Menu de Opções
opcao = st.sidebar.selectbox("O que deseja registrar?", [
    "Início",
    "Cadastrar Produto/Validade",
    "Produção Diária/Mensal",
    "Estoque",
    "Vendas e Pedidos",
    "Perdas",
    "Fornecedores & Análises"
])

# --- LOOP DE ENTRADA DE DADOS ---

if opcao == "Início":
    st.write("### Bem-vindo ao Sistema de Monitoramento.")
    st.info("Selecione uma categoria na barra lateral para inserir dados.")
    
    # Exibir últimos registros do banco
    conn = sqlite3.connect(DB_NAME)
    try:
        ultimos = pd.read_sql("SELECT * FROM registros ORDER BY id DESC LIMIT 5", conn)
        st.subheader("Últimas Movimentações")
        st.table(ultimos)
    except:
        st.write("Nenhum dado registrado ainda.")
    conn.close()

elif opcao == "Cadastrar Produto/Validade":
    with st.form("form_produto"):
        nome = st.text_input("Nome da Ração")
        animal = st.selectbox("Para qual animal?", ["Bovinos", "Suínos", "Aves", "Pets"])
        peso = st.number_input("Peso da Embalagem (kg)", min_value=0.0)
        fab = st.date_input("Data de Fabricação")
        val = st.date_input("Data de Validade")
        
        if st.form_submit_button("Salvar Produto"):
            dados = {"nome": nome, "tipo_animal": animal, "peso": peso, "fabricacao": fab, "validade": val}
            salvar_no_db("produtos", dados)
            st.success(f"Produto {nome} registrado com sucesso!")

elif opcao == "Produção Diária/Mensal":
    with st.form("form_producao"):
        tipo = st.selectbox("Tipo de Registro", ["Produção Diária", "Produção Mensal"])
        qtd = st.number_input("Quantidade Total (kg)", min_value=0.0)
        
        if st.form_submit_button("Registrar no Sistema"):
            dados = {
                "categoria": tipo,
                "detalhes": f"Registro de produção de ração",
                "quantidade": qtd,
                "data_registro": datetime.now()
            }
            salvar_no_db("registros", dados)
            st.success("Produção atualizada!")

elif opcao == "Vendas e Pedidos":
    with st.form("form_vendas"):
        tipo_venda = st.radio("Tipo", ["Venda Direta", "Pedido de Ração"])
        valor = st.number_input("Valor total (R$)", min_value=0.0)
        obs = st.text_input("Cliente/Detalhes")
        
        if st.form_submit_button("Finalizar Lançamento"):
            dados = {
                "categoria": tipo_venda,
                "detalhes": obs,
                "quantidade": valor,
                "data_registro": datetime.now()
            }
            salvar_no_db("registros", dados)
            st.balloons()
            st.success("Venda/Pedido salvo no banco de dados.")

# --- BOTÃO DE "DESLIGAR" (Encerramento da Sessão) ---
st.sidebar.markdown("---")
if st.sidebar.button("🔴 Desligar Sistema na Fábrica"):
    st.warning("Encerrando conexão com o banco de dados e fechando interface...")
    st.stop() # Interrompe a execução do script Streamlit
