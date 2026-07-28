from utils.observacoes import adicionar_observacao


def validar_nf_cancelada(df):

    # ==============================
    # Retorno SEFAZ
    # ==============================

    retorno_sefaz = (
        df["Retorno SEFAZ"]
        .fillna(0)
    )

    filtro_retorno = (
        (retorno_sefaz > 0) &
        (retorno_sefaz != 100)
    )

    # ==============================
    # Data de cancelamento
    # ==============================

    data_cancelamento = (
        df["Dt. Canc."]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    filtro_data = (
        (data_cancelamento != "") &
        (data_cancelamento != "/  /")
    )

    # ==============================
    # Observação
    # ==============================

    observacao = (
        df["Observacao"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    filtro_observacao = observacao.str.contains(
        "NF CANCELADA",
        na=False
    )

    # ==============================
    # Filtro Final
    # ==============================

    filtro = (
        filtro_retorno |
        filtro_data |
        filtro_observacao
    )

    return adicionar_observacao(
        df,
        filtro,
        "Verifique se a NF está cancelada"
    )
