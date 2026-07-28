import pandas as pd

from configs.aliquotas import ALIQUOTAS_INTERESTADUAIS



def calcular_icms_complementar(df, dados_unidade):

    df = df.copy()


    # ======================================
    # Conversão segura de números
    # ======================================

    def converter_numero(valor):

        if pd.isna(valor):
            return 0


        # Já veio como número do Excel/pandas
        if isinstance(valor, (int, float)):
            return valor


        valor = str(valor).strip()


        if valor == "":
            return 0


        # Texto brasileiro
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
    # Colunas de saída
    # ======================================

    colunas = [

        "Base ICMS Ajustada",
        "ICMS Complementar",
        "FCP",
        "Alíquota Interestadual Esperada",
        "Alíquota Interestadual Utilizada"

    ]


    for coluna in colunas:

        if coluna not in df.columns:

            df[coluna] = 0.0



    # ======================================
    # Dados da unidade destino
    # ======================================

    estado_destino = str(
        dados_unidade["estado"]
    ).strip().upper()


    aliquota_interna = float(
        dados_unidade["aliquota_interna"]
    )


    fcp = float(
        dados_unidade["fcp"]
    )



    # ======================================
    # Normalizações
    # ======================================

    df["CFOP"] = (

        df["CFOP"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()

    )


    df["Estado"] = (

        df["Estado"]
        .astype(str)
        .str.upper()
        .str.strip()

    )



    # ======================================
    # Valor Contábil
    # ======================================

    df["Vlr Contabil"] = (

        df["Vlr Contabil"]
        .apply(converter_numero)

    )



    # ======================================
    # Valor ICMS Complementar informado
    # ======================================

    df["Vlr ICMS Com"] = (

        df["Vlr ICMS Com"]
        .apply(converter_numero)

    )



    # ======================================
    # Cálculo
    # ======================================

    for index, row in df.iterrows():


        cfop = row["CFOP"]


        descricao = str(
            row.get("Desc. Produto", "")
        ).upper()



        # Apenas CFOP válidos

        if cfop not in [
            "2556",
            "2352",
            "2551"
        ]:

            continue



        # 2352 somente Frete Diversos

        if cfop == "2352":

            if "16.02" not in descricao:

                continue



        base = float(
            row["Vlr Contabil"]
        )



        if base <= 0:

            continue



        uf_origem = row["Estado"]



        aliquota_interestadual = (

            ALIQUOTAS_INTERESTADUAIS
            .get(uf_origem, {})
            .get(estado_destino, 12)

        )



        diferenca = (

            aliquota_interna -
            aliquota_interestadual

        )



        if diferenca <= 0:

            continue



        divisor = 1 - (

            aliquota_interna / 100

        )



        if divisor <= 0:

            continue



        # ======================================
        # Base por dentro
        # ======================================

        base_ajustada = (

            base / divisor

        )



        # ======================================
        # ICMS Complementar
        # ======================================

        icms_complementar = (

            base_ajustada *
            (diferenca / 100)

        )



        # ======================================
        # FCP
        # ======================================

        valor_fcp = (

            base_ajustada *
            (fcp / 100)

        )



        # ======================================
        # Alíquota utilizada fornecedor
        # ======================================

        valor_icms_com = float(
            row["Vlr ICMS Com"]
        )


        aliquota_utilizada = 0



        if base_ajustada > 0:


            aliquota_utilizada = (

                aliquota_interna -
                (
                    valor_icms_com /
                    base_ajustada
                ) * 100

            )



        # ======================================
        # Grava resultados
        # ======================================

        df.at[index, "Base ICMS Ajustada"] = round(
            base_ajustada,
            2
        )


        df.at[index, "ICMS Complementar"] = round(
            icms_complementar,
            2
        )


        df.at[index, "FCP"] = round(
            valor_fcp,
            2
        )


        df.at[index, "Alíquota Interestadual Esperada"] = round(
            aliquota_interestadual,
            2
        )


        df.at[index, "Alíquota Interestadual Utilizada"] = round(
            aliquota_utilizada,
            2
        )


    return df
