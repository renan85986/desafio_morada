import sqlite3

conn = sqlite3.connect("desafio_local.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE lead (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   nome TEXT UNIQUE NOT NULL,
   email TEXT UNIQUE ,
   telefone TEXT,
   orcamento REAL,
   localizacao TEXT,
   tipo_imovel TEXT,
   preferencias TEXT,
   duvidas TEXT
);
                     
CREATE TABLE empreendimentos (
   id INTEGER NOT NULL,
   nome TEXT UNIQUE NOT NULL,
   descricao TEXT UNIQUE ,
   localizacao TEXT,
   valor REAL,
   quartos INTEGER,
   banheiros INTEGER,
   area REAL,
   vagas INTEGER,
   caracteristicas TEXT,
   PRIMARY KEY (id, nome)
);

""")


conn.commit()
conn.close()

print("Banco de dados criado com sucesso")