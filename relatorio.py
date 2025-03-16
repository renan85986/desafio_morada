import streamlit as st
import pandas as pd
import sqlite3

def carregar_dados():
    conn = sqlite3.connect('D:/Pessoal/desafio_morada/bd/desafio_local.db')  
    df_leads = pd.read_sql("SELECT * FROM lead", conn)
    df_sugestoes = pd.read_sql("SELECT * FROM sugestoes", conn)
    df_empreendimentos = pd.read_sql("SELECT * FROM empreendimentos", conn)
    conn.close()
    return df_leads, df_sugestoes, df_empreendimentos

df_leads, df_sugestoes, df_empreendimentos = carregar_dados()

st.title("Relatório de Leads e Sugestões de Empreendimentos")

lead_selecionado = st.selectbox(" Selecione um Lead:", df_leads["nome_lead"])

df_leads = df_leads.set_index("id")


lead_info = df_leads[df_leads["nome_lead"] == lead_selecionado]
st.write("### Informações do Lead", lead_info)

df_sugestoes = df_sugestoes.set_index("id")
sugestao = df_sugestoes[df_sugestoes["nome_lead"] == lead_selecionado]
st.write("### Empreendimento Sugerido", sugestao)

if not sugestao.empty:
    empreendimento_info = df_empreendimentos[df_empreendimentos["nome"] == sugestao.iloc[0]["nome"]]
    st.write("### Detalhes do Empreendimento", empreendimento_info)

