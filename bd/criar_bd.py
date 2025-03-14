import sqlite3

conn = sqlite3.connect("desafio_local.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS lead (
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
                     


""")


conn.commit()
conn.close()

print("Banco de dados criado com sucesso")