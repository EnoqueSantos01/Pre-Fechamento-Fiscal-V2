COLUNAS_OBRIGATORIAS = [
    "CFOP",
    "Chave Doc",
    "Vlr. ICMS",
    "Filial"
]


def validar_colunas(df):

    faltando = []

    for coluna in COLUNAS_OBRIGATORIAS:

        if coluna not in df.columns:
            faltando.append(coluna)

    if faltando:

        raise Exception(
            f"Colunas obrigatórias ausentes: {', '.join(faltando)}"
        )