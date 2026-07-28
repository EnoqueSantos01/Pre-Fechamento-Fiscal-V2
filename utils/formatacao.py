def formatar_chaves(df):

    df["Chave Doc"] = (
        df["Chave Doc"]
        .fillna("")
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    return df

def validar_chaves(df):

    chave = df["Chave Doc"].fillna("").astype(str)

    filtro = (
        (chave != "") &
        (chave.str.len() != 44)
    )

    df.loc[filtro, "Observacoes"] += "Chave inválida; "

    return df


def formatar_cfop(df):

    if "CFOP" in df.columns:

        df["CFOP"] = (
            df["CFOP"]
            .fillna("")
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

    return df