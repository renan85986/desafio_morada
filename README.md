# Gerador de relatório de leads e empreendimentos

# Introdução
Em um contexto de mercado imobiliário, saber oferecer os melhores empreendimentos é fundamental para o corretor de imóveis. Pensando nisso, essa solução analisa conversas entre um lead (potencial cliente) e um assistente virtual, extrai os dados pertinentes dos 
leads, e gera um relatório contendo os dados dos clientes e baseado nesses dados, sugestões individuais de empreendimentos baseados nas informações fornecidas. O relatório também conta com várias análises gráficas quanto ao perfil geral dos leads, tipos de imóveis e geolocalização, além de fazer uma análise do sentimento e intenção de compra do lead, fornecendo uma ferramenta completa para o corretor orientar seu atendimento ao cliente.

** Observação: Para as instruções de como configurar a chave API do Gemini e executar o projeto, refira ao último item desse documento ("Configuração do ambiente")
# 1 - Tecnologias utilizadas
   - Python para processamento de dados
   - Pandas para manipulação das tabelas de dados e dataframes
   - Matplotlib e Seaborn para visualização dos dados
   - Sqlite para gerenciamento de banco de dados
   - API do google gemini, para gerar análises e extrair dados a partir das conversas simuladsa
   - Streamlit para visualização de forma organizada e visual

# 2 - Fluxo de Funcionamento
   ### 1. Entrada de dados: 
   conversas_leads.csv, contendo id e conteúdo da conversa
   
   empreendimentos.csv, contendo id, nome, descricao, localizacao, valor, quartos, banheiros, area, vagas, caracteristicas

   ### 2. Processamento de dados:
   Após ler os arquivos, as conversas são estruturadas em um dataframe e é requisitado ao Gemini para extrair informações de cada lead de cada conversa (nome, email, telefone, orçamento, localização, estado, tipo de imóvel, preferencias, dúvidas, sentimento em relação     ao serviço, e intenção de compra)


# 1 - Configuração do ambiente 

Antes de rodar o código, é necessário configurar a chave da API do Google no seu ambiente. Siga os passos abaixo para garantir que o código tenha acesso a ela:

### 1. Criar um projeto no Google Cloud
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
   - Crie um novo projeto ou selecione um existente.

### 2. AtivarSecret Manager
   - No Google Cloud Console, acesse **APIs & Services** > **Library**.
   - Pesquise e ativar a API **Secret Manager**.

### 3. Armazenar a chave da API no Secret Manager
   - Na barra de pesquisa do google cloud console, acesse **Secret Manager**.
   - Clique em **Create Secret** e insira a chave da API (do Google) como o valor do segredo.
   - Nomeie o segredo como `GOOGLE_API_KEY`.

### 4. Criar uma Conta de Serviço e gerar as credenciais
   - Procurar **IAM & Admin** > **Service Accounts**.
   - Clique em **Create Service Account** e forneça um nome.
   - Em permissões, adicione a função **Secret Manager Secret Accessor**(importante!!!)
   - Na aba **Keys**, gere uma chave no formato JSON
   - Baixe o arquivo JSON das credenciais

### 5. Configuração das variáveis de ambiente
   - Defina a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` com o caminho do arquivo JSON das credenciais baixadas:

     **No Windows (CMD):**
     ```cmd
     set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho_para_credenciais\credencial.json
     ```
     **No Linux/macOS:**
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/arquivo/credenciais.json"
     ```

  - Defina a variável de ambiente `GCP_PROJECT_ID` com o nome do arquivo de projeto do google cloud (normalmente aparece em visão geral do google cloud)
     ```cmd
     set GCP_PROJECT_ID=exemploexemplo-1203123-exemplo
     ```

  Se definir as variáveis no terminal, elas só valerão para a sessão atual do terminal (!!!)
  
  Por experiência própria, não dá para setar a variável no terminal do vscode, também não testei no powershell
  apenas no cmd. 
  
  Para checar as variáveis:
     ```cmd
     echo %variavel%
     ```
### 6. Instalar o Google Cloud SDK 
   - Baixar e instalar: [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - Depois, seguir:
     ```bash
     gcloud auth application-default login
     ```
     Isso permitirá autenticar e validar suas credenciais.

### 7. Instalar as dependências do projeto
   - Para rodar o código, instale as bibliotecas necessárias com o comando:
     ```bash
     pip install -r requirements.txt
     ```
   - Caso dê erro, instale as bibliotecas manualmente
     ```bash
     pip install pandas
     pip install google-generativeai
     pip install google-cloud-secret-manager
     pip install streamlit
     pip install matplotlib
     pip install plotly
     pip install numpy
     ```
     
### 8. Rodando o código
   Agora você pode rodar o código. Ele irá acessar automaticamente a chave da API do Google armazenada no Secret Manager.
   ```bash
   python main.py
   ```

### Solução de Problemas
- **Erro de credenciais**: Se o código falhar ao acessar a chave, verifique se a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` está configurada corretamente.
- **Permissões insuficientes**: Certifique-se de que a conta de serviço tem acesso ao segredo no Secret Manager.
- **Comando `gcloud` não encontrado**: Precisa instalar o google cloud SDK.

Seguindo esses passos, sua chave de API estará corretamente configurada e acessível para uso no código.




