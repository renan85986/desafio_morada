import pandas as pd
import google.generativeai as genai
import os

API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key = API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

conversas = pd.read_csv("D:/Pessoal/desafio_morada/dados/conversas_leads.csv")
primeira_conv = conversas.iloc[0,1]
print(conversas.iloc[0,1])

pergunta = f""" 
            Extraia as seguintes informações da conversa:
            - Nome do cliente
            - Orçamento
            Conversa : {primeira_conv}
            """

resposta = model.generate_content(pergunta)
print(resposta.text)