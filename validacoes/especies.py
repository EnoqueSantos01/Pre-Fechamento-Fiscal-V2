from utils.observacoes import adicionar_observacao


# =====================================================
# CFOPs válidos por espécie
# =====================================================

CFOP_VALIDOS = {

    "CTE": {
        "1352",
        "2352",
        "2932",
        "1932",
        "1353"
    },

    "NFCEE": {
        "1252",
        "2252"
    },

    "NFS": {
        "1933",
        "2933"
    },

    "NFSC": {
        "1302",
        "2302"
    },

    "NTST": {
        "1302",
        "2302",
        "1303",
        "2303"
    }

}


# =====================================================
# Validação CFOP x Espécie
# =====================================================

def validar_especie_cfop(df):

    especie = (
        df["Especie"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    cfop = (
        df["CFOP"]
        .fillna("")
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    filtro = df.index.map(

        lambda i:

        (
            especie.iloc[i] in CFOP_VALIDOS
            and cfop.iloc[i] not in CFOP_VALIDOS[
                especie.iloc[i]
            ]
        )

    )

    return adicionar_observacao(

        df,

        filtro,

        "CFOP incompatível com a espécie do documento"

    )


# =====================================================
# NFCOM deve possuir chave
# =====================================================

def validar_nfcom_chave(df):

    especie = (
        df["Especie"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    chave = (
        df["Chave Doc"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    filtro = (
        (especie == "NFCOM") &
        (chave == "")
    )

    return adicionar_observacao(

        df,

        filtro,

        "NFCOM deve possuir Chave"

    )
