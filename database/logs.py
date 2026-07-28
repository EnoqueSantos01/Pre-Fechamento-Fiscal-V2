import json
from datetime import datetime
import os

ARQUIVO = "database/logs.json"


def salvar_log(usuario, unidade, arquivo_nome, resumo=None):

    log = {
        "usuario": usuario,
        "unidade": unidade,
        "arquivo": arquivo_nome,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resumo": resumo or {}
    }

    if os.path.exists(ARQUIVO):

        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)

    else:
        dados = []

    dados.append(log)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)