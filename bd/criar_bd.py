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
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso")