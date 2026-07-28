import json


def carregar_usuarios():

    with open(
        "database/usuarios.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)