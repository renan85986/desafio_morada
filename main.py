import pandas as pd
import google.generativeai as genai
import time
import json
import re
import os
import sqlite3

API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key = API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') #mudei para o flash pq tava dando problema de quantidade de req

def extracao_info(conversa):
    pergunta = f""" 
                Extraia as seguintes informações da conversa:
                - Nome (string)
                - Email (string)
                - Contato (string)
                - Orçamento (inteiro)
                - Localização (string)
                - Tipo_imóvel (string)
                - Preferencias (string)
                - Duvidas_mencionadas (string)
                Conversa : {conversa}
                Responda estritamente em formato JSON válido e lembre de retornar o orçamento em formato compatível com banco de dados
                Retorne localização, preferencias e duvidas mencionadas como strings unicas, separando multiplicidades por virgula
                """
    resposta = model.generate_content(pergunta)
    resposta = re.sub(r"^```json|```$", "", resposta.text.strip()).strip()

    #print(resposta)
    dados = json.loads(resposta) #conversão para dicionário
    #print(type(dados))

    return dados

def processa_dados(conversas):
    dados_processados = [] # lista vazia

    for index, row in conversas.iterrows():
        conv = conversas.iloc[index,1]
        time.sleep(1)

        resp = extracao_info(conv)
        #print(resp)

        if resp:
            dados_processados.append(resp) # adiciona os dados processados à lista

        df_resp = pd.DataFrame(dados_processados) # transforma a lista em df
        print (df_resp)

    return df_resp    

def escrever_lead(dataframe):
    conn = sqlite3.connect('D:/Pessoal/desafio_morada/bd/desafio_local.db')
    cursor = conn.cursor()

    for _, row in dataframe.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO lead (nome, email, telefone, orcamento, localizacao, tipo_imovel, preferencias, duvidas) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Nome"], 
            row["Email"], 
            row["Contato"], 
            row["Orçamento"], 
            row["Localização"], 
            row["Tipo_imóvel"], 
            row["Preferencias"], 
            row["Duvidas_mencionadas"]        
        ))

    conn.commit()
    conn.close()
    print("banco de dados carregado com  sucesso!")

def escrever_empreendimentos(dataframe):
    dataframe = dataframe.set_index("id") #transformei o indice na coluna id

    try:
        conn = sqlite3.connect('D:/Pessoal/desafio_morada/bd/desafio_local.db')
        dataframe.to_sql("empreendimentos", con=conn, if_exists="append", index=False)
        conn.close()
        print("dados inseridos com sucesso!")
    except sqlite3.IntegrityError:
        print("Dados repetidos, foram ignorados")

    

conversas = pd.read_csv("D:/Pessoal/desafio_morada/dados/conversas_leads.csv")
df_resp = processa_dados(conversas)
escrever_lead(df_resp)

df_empreendimentos = pd.read_csv("D:/Pessoal/desafio_morada/dados/empreendimentos.csv")
print(df_empreendimentos)
escrever_empreendimentos(df_empreendimentos)

for index, row  in df_resp.iterrows():
    time.sleep(10)
    pergunta = f""" 
                    Baseado nas informações do lead (possível cliente), sugira um empreendimento, baseado na tabela de empreendimentos,
                    que seja adequado ao perfil e aos requisitos do cliente, retorne apenas uma string com o nome e o id do empreendimento e o lead correspondente
                    Também justifique sua escolha
                    Informações do lead : {row[:]}
                    Informações dos empreendimentos : {df_empreendimentos}
                    """
    resposta = model.generate_content(pergunta)
    print(resposta.text)
