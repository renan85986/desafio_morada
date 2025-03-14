import pandas as pd
import google.generativeai as genai
import time
import json
import re
import os

API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key = API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def extracao_info(conversa):
    pergunta = f""" 
                Extraia as seguintes informações da conversa:
                - Nome
                - Email
                - Contato
                - Orçamento
                - Localização 
                - Tipo_imóvel
                - Preferencias
                - Duvidas mencionadas
                Conversa : {conversa}
                Responda estritamente em formato JSON válido, sem caracteres extras como '''json ou '''' 
                e lembre de retornar o orçamento em formato compatível com banco de dados
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
        time.sleep(5)

        resp = extracao_info(conv)
        #print(resp)
        
        if resp:
            dados_processados.append(resp) # adiciona os dados processados à lista

        df_resp = pd.DataFrame(dados_processados) # transforma a lista em df
        print (df_resp.head())

    return df_resp    
    

conversas = pd.read_csv("D:/Pessoal/desafio_morada/dados/conversas_leads.csv")
processa_dados(conversas)


