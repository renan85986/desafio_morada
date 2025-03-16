import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
lead_info = df_leads.loc[df_leads["nome_lead"] == lead_selecionado, ["nome_lead", "email", "telefone", "orcamento", "localizacao", "estado", "tipo_imovel", "preferencias"]]
st.write("### Informações do Lead", lead_info)

df_sugestoes = df_sugestoes.set_index("id")
sugestao = df_sugestoes[df_sugestoes["nome_lead"] == lead_selecionado]
st.write("### Empreendimento Sugerido", sugestao)

if not sugestao.empty:
    empreendimento_info = df_empreendimentos.loc[df_empreendimentos["nome"] == sugestao.iloc[0]["nome"],["nome","localizacao","valor","quartos","banheiros","area","vagas","caracteristicas"]]
    st.write("### Detalhes do Empreendimento", empreendimento_info)

st.markdown("---")
#estado_selecionado = st.selectbox(" Selecione um estado: ", df_leads["nome_lead"])
lead_por_estado = df_leads["estado"].value_counts()

fig, ax = plt.subplots()
lead_por_estado.plot(kind="bar", ax=ax, color="royalblue")
ax.set_title("Leads por Localização")
ax.set_xlabel("Estado")
ax.set_ylabel("Quantidade")

st.pyplot(fig)