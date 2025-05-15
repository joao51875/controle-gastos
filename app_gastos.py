import streamlit as st
import pandas as pd
from datetime import date
import os

ARQUIVO_DADOS = 'controle_gastos.csv'

# Menu lateral
st.sidebar.title("Menu")
pagina = st.sidebar.radio("Ir para:", ["Página Inicial", "Registrar Gastos", "Gráficos"])

# Página inicial
if pagina == "Página Inicial":
    st.title("Bem-vindo ao Controle de Gastos!")
    st.write("Use o menu lateral para navegar entre registrar um gasto ou ver gráficos.")

# Página de registro
elif pagina == "Registrar Gastos":
    st.title("Registrar Gastos e Rendas")
    with st.form("form_gastos"):
        data = st.date_input("Data", value=date.today())
        tipo = st.selectbox("Tipo", ["Gasto", "Renda"])
        categoria = st.text_input("Categoria")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
        forma_pagamento = st.selectbox("Forma de Pagamento", ["Crédito", "Débito", "Pix", "Dinheiro", "Transferência", "Entrada em conta"])
        observacoes = st.text_area("Observações", height=70)
        
        enviar = st.form_submit_button("Registrar")
    
    if enviar:
        nova_linha = {
            "Data": data.strftime("%d/%m/%Y"),
            "Tipo": tipo,
            "Categoria": categoria,
            "Descrição": descricao,
            "Valor R$": valor,
            "Forma de pagamento": forma_pagamento,
            "Observações": observacoes
        }

        if os.path.exists(ARQUIVO_DADOS):
            df_existente = pd.read_csv(ARQUIVO_DADOS)
            df_novo = pd.concat([df_existente, pd.DataFrame([nova_linha])], ignore_index=True)
        else:
            df_novo = pd.DataFrame([nova_linha])
        
        df_novo.to_csv(ARQUIVO_DADOS, index=False)
        st.success("Registro salvo com sucesso!")

# Página de gráficos (por enquanto simples)
elif pagina == "Gráficos":
    st.title("Gráficos de Gastos e Rendas")
    if os.path.exists(ARQUIVO_DADOS):
        df = pd.read_csv(ARQUIVO_DADOS)
        df["Valor R$"] = pd.to_numeric(df["Valor R$"], errors='coerce')
        gastos = df[df["Tipo"] == "Gasto"]
        if not gastos.empty:
            st.bar_chart(gastos.groupby("Categoria")["Valor R$"].sum())
        else:
            st.info("Nenhum gasto registrado ainda.")
    else:
        st.warning("Nenhum dado encontrado.")