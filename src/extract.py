from pathlib import Path

import pandas as pd


def extrair_usuarios():
    # Localiza o CSV a partir da pasta principal do projeto.
    pasta_projeto = Path(__file__).resolve().parent.parent
    caminho_csv = pasta_projeto / "data" / "usuarios.csv"

    df = pd.read_csv(
        caminho_csv,
        encoding="utf-8",
        dtype={
            "account_number": str,
            "account_agency": str,
            "card_number": str,
        },
    )

    return df.to_dict(orient="records")


if __name__ == "__main__":
    usuarios = extrair_usuarios()

    for usuario in usuarios:
        print(usuario)