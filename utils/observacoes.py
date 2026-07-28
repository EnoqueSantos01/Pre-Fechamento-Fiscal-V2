def adicionar_observacao(df, filtro, mensagem):

    if "Observacoes" not in df.columns:
        df["Observacoes"] = ""

    df["Observacoes"] = df["Observacoes"].fillna("").astype(str)

    # validação REAL do filtro
    if not hasattr(filtro, "shape"):
        raise Exception(f"Filtro inválido: tipo {type(filtro)} recebido")

    if len(filtro) != len(df):
        raise Exception("Filtro inválido: tamanho diferente do DataFrame")

    filtro = filtro.fillna(False).astype(bool)

    df.loc[filtro, "Observacoes"] = (
        df.loc[filtro, "Observacoes"].astype(str)
        + mensagem
        + "; "
    )

    return df