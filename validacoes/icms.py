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
    # Conversão segura de valores
    # ======================================

    def converter_numero(valor):

        if pd.isna(valor):
            return 0


        # Já é número vindo do Excel/pandas
        if isinstance(valor, (int, float)):
            return valor


        valor = str(valor).strip()


        if valor == "":
            return 0


        # Caso venha texto brasileiro
        # Ex: 1.234,56

        if "," in valor:

            valor = (
                valor
                .replace(".", "")
                .replace(",", ".")
            )


        try:

            return float(valor)

        except:

            return 0



    # ======================================
    # Base ICMS
    # ======================================

    df["Base Icms"] = (
        df["Base Icms"]
        .apply(converter_numero)
    )



    # ======================================
    # Alíquota
    # ======================================

    df["Aliq ICMS."] = (
        df["Aliq ICMS."]
        .apply(converter_numero)
    )



    # ======================================
    # ICMS Informado
    # ======================================

    df["Vlr. ICMS"] = (
        df["Vlr. ICMS"]
        .apply(converter_numero)
    )



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
        .round(2)
    )



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
