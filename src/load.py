import sqlite3
from pathlib import Path

def carregar_usuarios(usuarios):
    pasta_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = pasta_projeto / "data" / "marketing.db"

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            name TEXT,
            mensagem TEXT,
            account_balance REAL,
            account_number TEXT,
            account_agency TEXT,
            card_number TEXT,
            account_id INTEGER,
            card_id INTEGER,
            account_limit REAL,
            card_limit REAL
        )
    ''')

    for usuario in usuarios:
        if not usuario.get("mensagem"):
            print(f"Usuário {usuario['id']} sem mensagem válida; não será salvo.")
            continue
        cursor.execute('''
            INSERT OR REPLACE INTO usuarios (
                id, name, mensagem, account_balance, account_number, 
                account_agency, card_number, account_id, card_id, 
                account_limit, card_limit
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            usuario["id"], usuario["name"], usuario["mensagem"], 
            usuario.get("account_balance"), usuario.get("account_number"), 
            usuario.get("account_agency"), usuario.get("card_number"), 
            usuario.get("account_id"), usuario.get("card_id"), 
            usuario.get("account_limit"), usuario.get("card_limit")
        ))

    conexao.commit()
    conexao.close()