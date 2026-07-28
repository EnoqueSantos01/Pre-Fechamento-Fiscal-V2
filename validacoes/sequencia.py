import pandas as pd

from utils.observacoes import adicionar_observacao


def validar_sequencia(df):

    if "Documento" not in df.columns or "Serie" not in df.columns:
        return df

    df = df.copy()

    df["Documento"] = pd.to_numeric(
        df["Documento"],
        errors="coerce"
    )

    df["Serie"] = (
        df["Serie"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    filtro = pd.Series(False, index=df.index)

    for serie in df["Serie"].unique():

        idx = df["Serie"] == serie

        documentos = df.loc[idx, "Documento"]

        quebra = (
            documentos.notna() &
            documentos.shift().notna() &
            (documentos != documentos.shift() + 1)
        )

        if not quebra.empty:
            quebra.iloc[0] = False

        filtro.loc[idx] = quebra

    return adicionar_observacao(
        df,
        filtro,
        "Possível quebra na sequência numérica"
    )
