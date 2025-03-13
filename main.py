import pandas as pd
import google.generativeai as genai
import time
import os

API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key = API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def extracao_info(conversa):
    pergunta = f""" 
                Extraia as seguintes informações da conversa:
                - Nome do cliente
                - Email
                - Contato
                - Orçamento
                - Localização desejada
                - Tipo de imóvel
                - Preferencias adicionais
                - Duvidas mencionadas
                Conversa : {conversa}
                Responda em formato JSON
                """
    resposta = model.generate_content(pergunta)
    return resposta.text


conversas = pd.read_csv("D:/Pessoal/desafio_morada/dados/conversas_leads.csv")

for index, row in conversas.iterrows():
    conv = conversas.iloc[index,1]
    time.sleep(15)
    resp = extracao_info(conv)
    print (resp)