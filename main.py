import pandas as pd
import google.generativeai as genai
from google.cloud import secretmanager
import time
import json
import re
import os
import sqlite3
import subprocess

def acessar_segredo(secret_name): #aquisição da chave de API
    client = secretmanager.SecretManagerServiceClient()

    project_id = os.getenv("GCP_PROJECT_ID")

    if not project_id:
        print("Variável de ambiente do project id ainda não foi definida")

    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    resposta = client.access_secret_version(name=secret_path)
    
    return resposta.payload.data.decode("UTF-8")

API_KEY = acessar_segredo('GOOGLE_API_KEY')

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
                - Estado (string)
                - Tipo_imóvel (string)
                - Preferencias (string)
                - Duvidas_mencionadas (string)
                - Sentimento (string)
                - Intenção (string)
                Conversa : {conversa}
                Responda estritamente em formato JSON válido e lembre de retornar o orçamento em formato compatível com banco de dados
                Retorne localização, preferencias e duvidas mencionadas como strings unicas, separando multiplicidades por virgula
                Para o campo estado, inferir a partir do campo localização, e retornar apenas a sigla do estado
                Para o campo sentimento, analise a conversa e classifique o sentimento do lead como: 'empolgado', 'neutro', 'desconfiado' ou 'insatisfeito', baseado nas respostas do lead
                Para o campo intenção, analise a conversa e classifique o interesse e intenção de compra do lead como: 'frio', 'morno' ou 'quente', baseado nas respostas do lead
                """
    resposta = model.generate_content(pergunta)
    resposta = re.sub(r"^```json|```$", "", resposta.text.strip()).strip() #retirada do "lixo" que tava atrapalhando a leitura da resposta

    dados = json.loads(resposta) 

    return dados

def processa_dados(conversas):
    dados_processados = [] 

    for index, row in conversas.iterrows():
        conv = conversas.iloc[index,1] #separando as conversas 
        time.sleep(1)

        resp = extracao_info(conv) #chamando por cada conversa

        if resp:
            dados_processados.append(resp) 

        df_resp = pd.DataFrame(dados_processados) 

    return df_resp    

def escrever_lead(dataframe):
    conn = sqlite3.connect('./bd/desafio_local.db')
    cursor = conn.cursor()

    for _, row in dataframe.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO lead (nome_lead, email, telefone, orcamento, localizacao, estado, tipo_imovel, preferencias, duvidas, sentimento, intencao) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (
            row["Nome"], 
            row["Email"], 
            row["Contato"], 
            row["Orçamento"], 
            row["Localização"],
            row["Estado"], 
            row["Tipo_imóvel"], 
            row["Preferencias"], 
            row["Duvidas_mencionadas"],
            row["Sentimento"],
            row["Intenção"]     
        ))

    conn.commit()
    conn.close()
    #print("banco de dados carregado com  sucesso!")

def escrever_empreendimentos(dataframe):
    dataframe = dataframe.set_index("id") #transformei o indice na coluna id

    dataframe["estado"] = dataframe["localizacao"].str[-2:] #extraindo ultimos 2 caracteres da coluna localização e criando coluna estado
    #print(dataframe)
   
    try:
        conn = sqlite3.connect('./bd/desafio_local.db')
        dataframe.to_sql("empreendimentos", con=conn, if_exists="append", index=False)
        conn.close()
        print("dados inseridos com sucesso!")
    except sqlite3.IntegrityError:
        print("Dados repetidos, foram ignorados")


def extracao_sugestao(lead, empreendimentos):
    dados_processados = []
    empreendimentos_lista = empreendimentos.to_dict(orient="records") #transformando dataframe em lista, já que não consigo iterar sobre ele
    empreendimentos_json = json.dumps(empreendimentos_lista, indent=4, ensure_ascii=False) #mandando em json para facilitar leitura 

    for index, row  in lead.iterrows():
        time.sleep(5)
        pergunta = f""" 
                        Baseado nas informações do lead (possível cliente), sugira o melhor empreendimento, considerando os critérios, nessa ordem:
                        1. O orçamento do lead deve ser compatível com o preço do empreendimento.
                        2. O tipo de imóvel desejado deve corresponder ao empreendimento.
                        3. O empreendimento deve estar localizado no mesmo estado do lead.
                        4. Se houver preferências específicas (como lazer, segurança, metragem), priorizar empreendimentos que atendam a esses critérios.
                        5. Se houver mais de um empreendimento adequado, escolha aquele com a menor diferença entre orçamento e preço do imóvel, mas apontar ambos na justificativa
                        6. Se não houver correspondência exata, sugerir o mais próximo, explicando a escolha
                        7. Considere também se é para compra ou aluguel

                        Retorne, estritamente em formato JSON:                       
                        -nome do empreendimento sugerido (nome)
                        -id do empreendimento (id)
                        - lead correspondente (nome_lead)
                        - justificativa 

                        Informações do lead : 
                        - Nome: {row["Nome"]}
                        - Orçamento do lead: {row["Orçamento"]}
                        - Localização: {row["Localização"]}
                        - Estado: {row["Estado"]}
                        - Tipo do imóvel: {row["Tipo_imóvel"]}
                        - Preferencias: {row["Preferencias"]}
                        
                        Informações dos empreendimentos : 
                        {empreendimentos_json}         
                        """
        resposta = model.generate_content(pergunta)
        resposta = re.sub(r"^```json|```$", "", resposta.text.strip()).strip()

        dados = json.loads(resposta)

        dados_processados.append(dados)
        df_sugestao = pd.DataFrame(dados_processados)

    return df_sugestao
   
def escrever_sugestao(dataframe):
    conn = sqlite3.connect('./bd/desafio_local.db')
    cursor = conn.cursor()

    for _, row in dataframe.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO sugestoes (nome_lead, id, nome, justificativa) 
            VALUES (?, ?, ?, ?)
        """, (
            row["nome_lead"], 
            row["id"], 
            row["nome"], 
            row["justificativa"]    
        ))

    conn.commit()
    conn.close()
    print("banco de dados carregado com  sucesso!") 

conversas = pd.read_csv("./dados/conversas_leads.csv")
print("Extraindo dados de conversa e realizando consultas...")
df_resp = processa_dados(conversas)
escrever_lead(df_resp)

df_empreendimentos = pd.read_csv("./dados/empreendimentos.csv")
print("Extraindo dados de empreendimentos e realizando consultas....")
escrever_empreendimentos(df_empreendimentos)
df_sugestao = extracao_sugestao(df_resp, df_empreendimentos)
escrever_sugestao(df_sugestao)

print("Gerando relatório....")
subprocess.run(["streamlit", "run", "relatorio.py"])