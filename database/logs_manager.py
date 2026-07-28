import json
import os
from datetime import datetime


def salvar_log(log):

    pasta = "database/logs"
    os.makedirs(pasta, exist_ok=True)

    data = datetime.now().strftime("%Y-%m-%d")
    caminho = f"{pasta}/{data}.json"

    if os.path.exists(caminho):

        with open(caminho, "r", encoding="utf-8") as f:
            logs = json.load(f)

    else:
        logs = []

    logs.append(log)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)