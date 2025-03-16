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

nome_leads = df_leads["nome_lead"].to_list()
#print(nome_leads)

orcamento_leads = df_leads["orcamento"].to_list()
#print(orcamento_leads)

empreendimentos_sugeridos = (df_sugestoes.loc[df_sugestoes["nome_lead"] == nome_leads, "nome"]).to_list()
orcamento_sugeridos = df_empreendimentos.loc[df_empreendimentos["nome"].isin(empreendimentos_sugeridos), "valor"].to_list() #isin verifica se os elementos da serie empreendimentos_sugeridos estão na coluna "nome"
#print(empreendimentos_sugeridos)
#print(orcamento_sugeridos)

st.markdown("---")
#estado_selecionado = st.selectbox(" Selecione um estado: ", df_leads["nome_lead"])
lead_por_estado = df_leads["estado"].value_counts()

empreendimentos_por_estado = df_empreendimentos["estado"].value_counts()

df_leads_filtrado = df_leads[~df_leads["tipo_imovel"].str.contains(",", na=False)]

cont_tipo_imovel = df_leads_filtrado["tipo_imovel"].value_counts()

df_comp = pd.DataFrame({"Leads": df_leads["estado"].value_counts(), 
                        "Empreendimentos": df_empreendimentos["estado"].value_counts()}).fillna(0)

figura, (ax, ax2) = plt.subplots(1,2)
lead_por_estado.plot(kind="bar", ax=ax, color="royalblue")
empreendimentos_por_estado.plot(kind="bar", ax=ax2, color="red")
ax.set_title("Leads por Estado")
ax.set_xlabel("Estado")
ax.set_ylabel("Quantidade")

ax2.set_title("Empreendimentos por Estado")
ax2.set_xlabel("Estado")
ax2.set_ylabel("Quantidade")

st.pyplot(figura)

fig3, ax4 = plt.subplots()
df_comp.plot(kind="bar", stacked=True, ax=ax4, color=["royalblue", "lightcoral"])
ax4.set_title("Leads vs. Empreendimentos por Estado")
ax4.set_xlabel("Estado")
ax4.set_ylabel("Quantidade")
st.pyplot(fig3)

fig2, ax3 = plt.subplots()
cont_tipo_imovel.plot(kind="bar", ax=ax3, color="royalblue")
ax3.set_title("Tipos de imóveis mais procurados")
ax3.set_xlabel("Tipo")
ax3.set_ylabel("Quantidade")
st.pyplot(fig2)