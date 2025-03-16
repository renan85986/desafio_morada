import sqlite3

conn = sqlite3.connect("desafio_local.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS lead (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   nome_lead TEXT UNIQUE NOT NULL,
   email TEXT UNIQUE ,
   telefone TEXT,
   orcamento REAL,
   localizacao TEXT,
   estado TEXT,
   tipo_imovel TEXT,
   preferencias TEXT,
   duvidas TEXT
);
                     
CREATE TABLE IF NOT EXISTS empreendimentos (
   id INTEGER,
   nome TEXT PRIMARY KEY NOT NULL,
   descricao TEXT ,
   localizacao TEXT,
   valor REAL,
   quartos INTEGER,
   banheiros INTEGER,
   area REAL,
   vagas INTEGER,
   caracteristicas TEXT
);

CREATE TABLE IF NOT EXISTS sugestoes (
   nome_lead TEXT NOT NULL,
   id INTEGER,
   nome TEXT,
   justificativa TEXT,
   PRIMARY KEY (nome_lead),
   FOREIGN KEY (nome_lead) REFERENCES lead(nome_lead),
   FOREIGN KEY (id) REFERENCES empreendimentos(id),   
   FOREIGN KEY (nome) REFERENCES empreendimentos(nome)   
);                  

""")


conn.commit()
conn.close()

print("Banco de dados criado com sucesso")