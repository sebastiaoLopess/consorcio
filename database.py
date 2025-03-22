import sqlite3

def conectar_banco():
    conn = sqlite3.connect("szabodb.db")
    return conn

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        usuario TEXT UNIQUE NOT NULL,
                        senha TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def registrar_usuario(nome, usuario, senha):
    senha_hash = senha
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)", 
                       (nome, usuario, senha_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validar_usuario(usuario, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario=?", (usuario,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return True
    return False