from utils.observacoes import adicionar_observacao


# =====================================================
# CSTs válidos por CFOP
# =====================================================

CST_VALIDOS = {

    # Uso e Consumo
    "1407": {"060"},
    "2407": {"060"},

    "1556": {"090"},
    "2556": {"090"},
    "2551": {"090"},

    # Energia Elétrica
    "1252": {"000"},
    "2252": {"000"},

    # Saídas sem destaque de ICMS
    "5556": {"040", "041"},
    "6556": {"040", "041"},

    # Venda sujeita à ST
    "6107": {"060"},
    "6108": {"060"}

}


# =====================================================
# Validação CFOP x CST
# =====================================================

def validar_cfop_cst(df):

    if "CFOP" not in df.columns or "Classif." not in df.columns:
        return df

    cfop = (
        df["CFOP"]
        .fillna("")
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    cst = (
        df["Classif."]
        .fillna("")
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(3)
        .str.strip()
    )

    filtro = df.index.map(

        lambda i:

        (
            cfop.iloc[i] in CST_VALIDOS
            and cst.iloc[i] not in CST_VALIDOS[cfop.iloc[i]]
        )

    )

    return adicionar_observacao(

        df,

        filtro,

        "CST incompatível com o CFOP"

    )
