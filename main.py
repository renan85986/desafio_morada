import pandas as pd
import google.generativeai as genai
import os

API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key = API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

resposta = model.generate_content("Olá google!")
print(resposta.text)