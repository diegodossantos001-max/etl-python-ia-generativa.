import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from src.extract import extrair_usuarios
from src.transform import validar_usuarios, gerar_mensagem
from src.load import carregar_usuarios


def main():
    pasta_projeto = Path(__file__).resolve().parent
    caminho_env = pasta_projeto / ".env"
    load_dotenv(caminho_env)

    chave_api = os.getenv("OPENAI_API_KEY")

    if chave_api:
        print("Chave configurada")
        cliente = OpenAI(api_key=chave_api)
    else:
        print("Chave não configurada")
        return
    usuarios = extrair_usuarios()
    usuarios_validos = validar_usuarios(usuarios)
    print(f"Total de Usuários válidos: {len(usuarios_validos)}")

    if not usuarios_validos:
        print("Nenhum usuário válido para gerar mensagens.")
        return
    for usuario in usuarios_validos:
        print(f"ID: {usuario['id']} | Nome: {usuario['name']}")
        mensagem = gerar_mensagem(cliente, usuario)

        if mensagem is not None:
            usuario["mensagem"] = mensagem
            print(mensagem)
            print(f"Quantidade de caracteres: {len(mensagem)}")
        else:
            print("Não foi obtida uma mensagem válida.")
    
    carregar_usuarios(usuarios_validos)
        

if __name__ == "__main__":
    main()