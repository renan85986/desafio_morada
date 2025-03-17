# Gerador de relatório de leads e sugestões de empreendimentos

# Introdução
Em um contexto de mercado imobiliário, saber oferecer os melhores empreendimentos é fundamental para o corretor de imóveis. Pensando nisso, essa solução analisa conversas entre um lead (potencial cliente) e um assistente virtual, extrai os dados pertinentes dos 
leads, e gera um relatório contendo os dados dos clientes e baseado nesses dados, sugestões individuais de empreendimentos baseados nas informações fornecidas. 

O relatório também conta com várias análises gráficas quanto ao perfil geral dos leads, tipos de imóveis e geolocalização, além de fazer uma análise do sentimento e intenção de compra do lead, fornecendo uma ferramenta completa para o corretor orientar seu atendimento ao cliente.

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
   Após ler os arquivos, as conversas são estruturadas em um dataframe e é requisitado ao Gemini para extrair informações de cada lead de cada conversa (nome, email, telefone, orçamento, localização, estado, tipo de imóvel, preferencias, dúvidas, sentimento em relação     ao serviço, e intenção de compra). [funções processa_dados() e extracao_info()] 
   
   Depois, as informações extraídas da conversa são inseridas no banco de dados, na tabela lead. [escrever_lead()]
   
   De forma semelhante, o dataframe salvo com os dados dos empreendimentos é salvo inteiro no banco de dados na tabela empreendimentos. [escrever_empreendimentos()] 

   Com os dados organizados, é feita uma outra requisição pro gemini, a partir dos dados do lead e dos empreendimentos, é requisitado ao gemini a melhor sugestão de empreendimento para cada lead, considerando as informações fornecidas pelo mesmo
   O gemini retorna o nome do empreendimento, assim como seu id, o lead correspondente e a justificativa para a escolha. [extracao_sugestao()]
   
   Novamente, os dados são persistidos no banco de dados na tabela sugestoes. [escrever_sugestoes()] 

   ### 3. Geração do relatório:
   Após extraídos os dados e persistidos no banco de dados, o código relatorio.py extrai os dados de cada tabela e gera insights e visualizações de acordo através do streamlit, são elas:
       - Informações do lead selecionado
       - Justificativa do empreendimento sugerido
       - Informações do empreendimento sugerido
       - Indicador de sentimento e intenção de compra
       - Comparativo entre orçamento do lead e valor do empreendimento sugerido
       
   Em seguida, são mostrados insights mais gerais de todos os leads:
       - Comparativo entre orçamento do lead e valor do empreendimento sugerido de todos 
       - Empreendimentos x Estado e Leads x Estado
       - Tipos de imóveis mais procurados
       
   <p align="center">
       <img src="https://github.com/user-attachments/assets/420fd7cc-fe4c-4e9d-a83a-8952c0f73e8c" width="45%">
       <img src="https://github.com/user-attachments/assets/11f3cc9f-dede-40f0-a9f6-d4664c23e434" width="45%">
   </p>
   <p align="center">
       <img src="https://github.com/user-attachments/assets/d091a0c4-ef85-4431-89a6-360533183367" width="45%">
       <img src="https://github.com/user-attachments/assets/6c0168be-c249-40df-8e51-000c84c91941" width="45%">
   </p>
       
# 3 - Banco de dados 
   O banco de dados utilizado é o SQLite, e foi escolhido devido a facilidade de compartilhar sua estrutura, visto que é baseado em arquivos.
   
   Por isso, o banco de dados já está corretamente configurado e com dados na pasta bd (desafio_local.db). Caso julgue necessário, é possível gerar novamente o banco ao rodar o script criar_bd.py, ele gerará o banco novamente e sem os dados, ao fazer isso mover o       
   arquivo do banco para a pasta bd para o correto funcionamento do código.

# 4 - Principais Desafios
   Apesar de ser um projeto de nível iniciante, foram enfrentados desafios interessantes devido ao uso de novas tecnologias e ao processamento de dados em linguagem natural. O projeto seguiu a opção 1 "Extrator de Informações de Conversas", porém contém algumas funcionalidades adicionais.
   
   Apesar da manipulação de tabelas e dataframes ser semelhante a outros projetos, o processamento 
   de dados em linguagem natural se provou um desafio interessante em relação à extração de informações relevantes dos textos, à normalização dos dados e à criação de regras para a recomendação do empreendimento ideal. A principal dificuldade foi interpretar 
   corretamente as preferências dos leads, que muitas vezes estavam descritas de maneira subjetiva ou ambígua. 

   Uma limitação da solução é quanto ao tempo de execução, como é usada uma versão gratuita da api do google gemini, o número de requisições à ela é limitado, por isso foram introduzidas algumas paradas temporárias entre uma requisição e outra, para não sobrecarregar e gerar erro

   Além disso, outro desafio foi estruturar a lógica de recomendação para que ela seguisse os critérios estabelecidos de forma eficiente, garantindo que o empreendimento sugerido fosse o mais adequado possível. Foi necessário definir uma ordem de prioridade clara e 
   implementar filtros progressivos para encontrar a melhor correspondência.

   Por fim, a criação do gráfico comparativo trouxe aprendizados na visualização de dados, especialmente na escolha adequada das cores, da disposição das barras e na apresentação clara da relação entre orçamento e preço do empreendimento.

   Apesar dos desafios, o projeto foi uma excelente oportunidade de aprendizado, consolidando conhecimentos em manipulação de dados, processamento de linguagem natural e visualização de informações.

# 5 - Conclusão
   A lógica fornece uma ferramenta valiosa para otimizar o processo de recomendação e tratamento de clientes no setor imobiliário.
   Como possíveis melhorias, o sistema pode ser aprimorado com modelos de aprendizado de máquina para tornar a recomendação mais dinâmica, além de incorporar pesos ajustáveis a cada critério, baseado nas informações extraidas do lead. 
   
   A análise de sentimento e intenção de compra é bem simples ainda e pode ser muito aprimorada, levando em vista também que as conversas utilizadas na análise não demonstravam muitos sinais emocionais ou subjetivos, o que é compreensivel se tratando de uma conversa simulada, porém com uma conversa real, com certeza essa funcionalidade vai ser mais explorada e gerará um insight poderoso para o corretor que o usar.

   O projeto final foi considerado satisfatório frente aos requisitos do desafio técnico e considerando o tempo para sua implementação. Foram exercitados conceitos de processamento de linguagem natural, análise e visualização de dados, suportado por modelos de 
   linguagem, no caso o Gemini.
   
# 6 - Configuração do ambiente 

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




