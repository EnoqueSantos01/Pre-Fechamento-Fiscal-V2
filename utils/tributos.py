from configs.aliquotas import ALIQUOTAS_INTERESTADUAIS


def obter_aliquota_interestadual(uf_origem: str, uf_destino: str):
    """
    Retorna a alíquota interestadual entre UF origem e destino.
    Ex: SP -> MG
    """

    try:
        return ALIQUOTAS_INTERESTADUAIS[uf_origem][uf_destino]
    except KeyError:
        return None


def obter_aliquota_interna(unidades: dict, filial: int):
    """
    Retorna a alíquota interna da unidade (UF origem).
    """

    try:
        return unidades[filial]["aliquota_interna"]
    except KeyError:
        return None


def calcular_difal(base: float, uf_origem: str, uf_destino: str, aliquota_interna: float):
    """
    Calcula DIFAL (ICMS Complementar básico).

    Fórmula:
        (aliquota_interna - aliquota_interestadual) * base
    """

    aliquota_inter = obter_aliquota_interestadual(uf_origem, uf_destino)

    if aliquota_inter is None:
        return None

    diferenca = aliquota_interna - aliquota_inter

    if diferenca < 0:
        diferenca = 0

    return base * (diferenca / 100)


def calcular_icms_interestadual(base: float, uf_origem: str, uf_destino: str):
    """
    Calcula ICMS interestadual simples.
    """

    aliquota = obter_aliquota_interestadual(uf_origem, uf_destino)

    if aliquota is None:
        return None

    return base * (aliquota / 100)


def calcular_icms_interno(base: float, aliquota_interna: float):
    """
    Calcula ICMS interno.
    """

    return base * (aliquota_interna / 100)
