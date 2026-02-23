import streamlit as st
import re

# Configuração da página
st.set_page_config(page_title="Ração Segura v0.1.0", layout="wide")

# --- FUNÇÃO DE VALIDAÇÃO DE SENHA ---
def validar_senha(senha):
    # Regra: 10 letras, 2 números, 1 caractere especial
    if len(senha) < 13: return False
    letras = len(re.findall(r'[a-zA-Z]', senha))
    numeros = len(re.findall(r'[0-9]', senha))
    especiais = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', senha))
    
    return letras >= 10 and numeros >= 2 and especiais >= 1

# --- BARRA LATERAL (Navegação) ---
st.sidebar.title("🛡️ Ração Segura v0.1.0")
menu = st.sidebar.selectbox("Navegação", [
    "Login", 
    "Produtos & Animais", 
    "Produção & Estoque", 
    "Qualidade & Fornecedores",
    "Vendas & Perdas"
])

# --- LÓGICA DAS TELAS ---

if menu == "Login":
    st.header("Acesso ao Sistema")
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password", help="10 letras, 2 números e 1 caractere especial")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            if validar_senha(senha):
                st.success(f"Bem-vindo, {usuario}!")
            else:
                st.error("Senha fora do padrão exigido!")

elif menu == "Produtos & Animais":
    st.header("Cadastro de Produtos")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome da Ração")
        st.selectbox("Tipo de Animal", ["Bovinos", "Suínos", "Aves", "Pets", "Outros"])
    with col2:
        st.date_input("Data de Fabricação")
        st.date_input("Data de Validade")
    st.button("Cadastrar Produto")

elif menu == "Produção & Estoque":
    st.header("Controle de Produção e Estoque")
    tab1, tab2 = st.tabs(["Produção Diária/Mensal", "Estoque"])
    
    with tab1:
        st.number_input("Quantidade Produzida (kg)", min_value=0)
        st.radio("Período", ["Diário", "Mensal"])
        st.button("Registrar Produção")
        
    with tab2:
        st.number_input("Peso Atual em Estoque (kg)", min_value=0)
        st.button("Atualizar Estoque")

elif menu == "Qualidade & Fornecedores":
    st.header("Análises e Parceiros")
    with st.expander("Nova Análise Laboratorial"):
        st.file_uploader("Upload do Laudo")
        st.text_area("Observações da Análise")
        st.button("Salvar Análise")
        
    with st.expander("Cadastrar Fornecedor"):
        st.text_input("Nome da Empresa / CNPJ")
        st.button("Cadastrar Fornecedor")

elif menu == "Vendas & Perdas":
    st.header("Movimentação Financeira e de Material")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Vendas e Pedidos")
        st.number_input("Valor da Venda (R$)", min_value=0.0)
        st.button("Registrar Venda/Pedido")
    with col_b:
        st.subheader("Perdas")
        st.number_input("Quantidade Perdida (kg)", min_value=0.0)
        st.text_input("Motivo da Perda")
        st.button("Registrar Perda")
