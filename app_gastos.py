import streamlit as st
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import tempfile

# Conectar ao Google Sheets
def conectar_planilha():
    escopo = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Converte st.secrets["credenciais"] para JSON string
    credenciais_json = json.dumps(st.secrets["credenciais"])

    # Salva temporariamente as credenciais
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as temp:
        temp.write(credenciais_json)
        temp.flush()
        gc = gspread.service_account(filename=temp.name)
        planilha = gc.open("controle_gastos")
        aba = planilha.worksheet("Dados")
        return aba

# Interface do app
st.title("Registro de Gastos e Rendas")

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
    try:
        aba = conectar_planilha()
        nova_linha = [
            data.strftime("%d/%m/%Y"),
            tipo,
            categoria,
            descricao,
            f"{valor:.2f}",
            forma_pagamento,
            observacoes
        ]
        aba.append_row(nova_linha, value_input_option="USER_ENTERED")
        st.success("Registro salvo com sucesso no Google Sheets!")
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar: {type(e).__name__}: {e}")
