def adicionar_observacao(df, filtro, mensagem):

    if "Observacoes" not in df.columns:
        df["Observacoes"] = ""

    df["Observacoes"] = (
        df["Observacoes"]
        .fillna("")
        .astype(str)
    )

    if not hasattr(filtro, "shape"):
        raise Exception(
            f"Filtro inválido: tipo {type(filtro)} recebido"
        )

    if len(filtro) != len(df):
        raise Exception(
            "Filtro inválido: tamanho diferente do DataFrame"
        )

    filtro = (
        filtro
        .fillna(False)
        .astype(bool)
    )

    def adicionar(valor):

        if mensagem in valor:
            return valor

        if valor.strip() == "":
            return mensagem + "; "

        return valor + mensagem + "; "

    df.loc[filtro, "Observacoes"] = (
        df.loc[filtro, "Observacoes"]
        .apply(adicionar)
    )

    return df
