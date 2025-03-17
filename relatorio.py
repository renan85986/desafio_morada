import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

largura = 0.30

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
lead_info_renomeado = lead_info.rename(columns={
    "nome_lead": "Nome do Lead",
    "email": "Email",
    "telefone": "Telefone",
    "orcamento": "Orçamento",
    "localizacao": "Localização",
    "estado": "Estado",
    "tipo_imovel": "Tipo de Imóvel",
    "preferencias": "Preferências"
})
st.write("### Informações do Lead", lead_info_renomeado)

df_sugestoes = df_sugestoes.set_index("id")
sugestao = df_sugestoes[df_sugestoes["nome_lead"] == lead_selecionado]
sugestao_renomeado = sugestao.rename(columns={
    "nome_lead": "Nome do Lead",
    "nome": "Nome do Empreendimento",
    "justificativa": "Justificativa",
})
st.write("### Empreendimento Sugerido", sugestao_renomeado)

if not sugestao.empty:
    empreendimento_info = df_empreendimentos.loc[df_empreendimentos["nome"] == sugestao.iloc[0]["nome"],["nome","localizacao","valor","quartos","banheiros","area","vagas","caracteristicas"]]
    empreendimento_info_renomeado = empreendimento_info.rename(columns={
        "nome": "Nome do Empreendimento",
        "localizacao": "Localização",
        "valor": "Valor",
        "quartos": "Quartos",
        "banheiros": "Banheiros",
        "area": "Área (m²)",
        "vagas": "Vagas",
        "caracteristicas": "Características"
    })
    st.write("### Detalhes do Empreendimento", empreendimento_info_renomeado)

#Gráfico interativo
st.write("### Orçamento do lead x Valor do empreendimento sugerido")
lead_orcamento = df_leads.loc[df_leads["nome_lead"] == lead_selecionado, "orcamento"].values[0]
nome_sugestao_atual = df_sugestoes.loc[df_sugestoes["nome_lead"] == lead_selecionado, "nome"].values[0]
sugerido_orcamento = df_empreendimentos.loc[df_empreendimentos["nome"] == nome_sugestao_atual, "valor"].values[0]

x = ['Orçamento do lead', 'Valor do imóvel']
valores = [lead_orcamento, sugerido_orcamento]

fig2, ax2 = plt.subplots(figsize=(10,5))

ax2.bar(x,valores, color=['royalblue','red'], width=largura)
st.pyplot(fig2)


st.markdown("---")

#Gráficos Gerais
st.write("### Insights Gerais")
nome_leads = df_leads["nome_lead"].to_list()

orcamento_leads = df_leads["orcamento"].to_list()

empreendimentos_sugeridos = []
orcamento_sugeridos = []

for nome_lead in nome_leads:
    empreendimentos = df_sugestoes.loc[df_sugestoes["nome_lead"] == nome_lead, "nome"].to_list()
    if empreendimentos: 
        empreendimento_sugerido = empreendimentos[0]  
        orcamento_empreendimento = df_empreendimentos.loc[df_empreendimentos["nome"] == empreendimento_sugerido, "valor"].to_list()
        if orcamento_empreendimento:
            empreendimentos_sugeridos.append(empreendimento_sugerido)
            orcamento_sugeridos.append(orcamento_empreendimento[0])  
        else:
            orcamento_sugeridos.append(0)  
    else:
        orcamento_sugeridos.append(0)  

fig, ax = plt.subplots(figsize=(19, 8))

r1 = np.arange(len(orcamento_leads))
r2 = [x + largura for x in r1]

ax.bar(r1, orcamento_leads, color='red', width=largura, label='Orçamento Lead')
ax.bar(r2, orcamento_sugeridos, color='blue', width=largura, label='Valor Empreendimento Sugerido')

ax.set_xlabel('Leads')
ax.set_ylabel('Orçamento')
ax.set_xticks([r + largura for r in range(len(orcamento_leads))])
ax.set_xticklabels(nome_leads)

ax.legend()

st.pyplot(fig)

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