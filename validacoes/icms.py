import pandas as pd


def calcular_icms(df):

    df = df.copy()

    # ======================================
    # Colunas de saída
    # ======================================

    colunas = [
        "ICMS Calculado",
        "Alíquota Informada",
        "Alíquota Calculada"
    ]

    for coluna in colunas:

        if coluna not in df.columns:
            df[coluna] = 0.0

    # ======================================
    # Base ICMS
    # ======================================

    df["Base Icms"] = (
        df["Base Icms"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["Base Icms"] = pd.to_numeric(
        df["Base Icms"],
        errors="coerce"
    ).fillna(0)

    # ======================================
    # Alíquota Informada
    # ======================================

    df["Aliq ICMS."] = (
        df["Aliq ICMS."]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["Aliq ICMS."] = pd.to_numeric(
        df["Aliq ICMS."],
        errors="coerce"
    ).fillna(0)

    # ======================================
    # ICMS Informado
    # ======================================

    df["Vlr. ICMS"] = (
        df["Vlr. ICMS"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["Vlr. ICMS"] = pd.to_numeric(
        df["Vlr. ICMS"],
        errors="coerce"
    ).fillna(0)

    # ======================================
    # ICMS Calculado
    # ======================================

    df["ICMS Calculado"] = (
        df["Base Icms"] *
        (df["Aliq ICMS."] / 100)
    ).round(2)

    # ======================================
    # Alíquota Informada
    # ======================================

    df["Alíquota Informada"] = (
        df["Aliq ICMS."]
    ).round(2)

    # ======================================
    # Alíquota Calculada
    # ======================================

    df["Alíquota Calculada"] = 0.0

    filtro = df["Base Icms"] > 0

    df.loc[filtro, "Alíquota Calculada"] = (
        (
            df.loc[filtro, "Vlr. ICMS"] /
            df.loc[filtro, "Base Icms"]
        ) * 100
    ).round(2)

    return df