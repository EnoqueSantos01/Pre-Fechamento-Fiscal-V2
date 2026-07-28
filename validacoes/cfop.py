from utils.observacoes import adicionar_observacao


def validar_cfop_2556_icms_st(df):

    filtro = (
        (df["CFOP"] == "2556") &
        (df["Icms Ret"] > 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 2556 não pode ter ICMS ST"
    )

    return df


def validar_cfop_1556_icms_st(df):

    filtro = (
        (df["CFOP"] == "1556") &
        (df["Icms Ret"] > 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 1556 não pode ter ICMS ST"
    )

    return df


def validar_cfop_2556_Vlr_ICMS_Com(df):

    filtro = (
        (df["CFOP"] == "2556") &
        (df["Vlr ICMS Com"] == 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 2556 não pode estar zerado o VLR ICMS Com"
    )

    return df


def validar_cfop_2551_Vlr_ICMS_Com(df):

    filtro = (
        (df["CFOP"] == "2551") &
        (df["Vlr ICMS Com"] == 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 2551 não pode estar zerado o VLR ICMS Com"
    )

    return df


def validar_cfop_2352_frete(df):

    filtro = (
        (df["CFOP"] == "2352") &
        (df["Desc. Produto"] == "16.02 - FRETE DIVERSOS") &
        (df["Vlr ICMS Com"] == 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "2352 com Frete para Uso e Consumo não pode estar zerado"
    )

    return df


def validar_cfop_5556_ICMS(df):

    filtro = (
        (df["CFOP"] == "5556") &
        (df["Vlr. ICMS"] > 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 5556 não pode estar com valor de ICMS"
    )

    return df


def validar_cfop_6556_ICMS(df):

    filtro = (
        (df["CFOP"] == "6556") &
        (df["Vlr. ICMS"] > 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 6556 não pode estar com valor de ICMS"
    )

    return df


def validar_cfop_5556_DIFAL_ICMS(df):

    filtro = (
        (df["CFOP"] == "5556") &
        (df["Difal ICMS"] > 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 5556 não pode estar com valor de DIFAL ICMS"
    )

    return df


def validar_cfop_6556_DIFAL_ICMS(df):

    filtro = (
        (df["CFOP"] == "6556") &
        (df["Difal ICMS"] > 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 6556 não pode estar com valor de DIFAL ICMS"
    )

    return df


def validar_cfop_6107_icms(df):

    filtro = (
        (df["CFOP"] == "6107") &
        (df["Icms Ret"] == 0) &
        (df["Difal ICMS"] == 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 6107: ICMS Ret ou Difal ICMS deve ter valor"
    )

    return df


def validar_cfop_6108_icms(df):

    filtro = (
        (df["CFOP"] == "6108") &
        (df["Icms Ret"] == 0) &
        (df["Difal ICMS"] == 0)
    )

    df = adicionar_observacao(
        df,
        filtro,
        "CFOP 6108: ICMS Ret ou Difal ICMS deve ter valor"
    )

    return df