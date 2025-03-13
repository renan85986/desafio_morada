import sqlite3

conn = sqlite3.connect("desafio_local.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE lead (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   nome TEXT NOT NULL,
   email TEXT,
   telefone TEXT,
   orcamento REAL,
   localizacao TEXT,
   tipo_imovel TEXT,
   preferencias TEXT
);
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso")