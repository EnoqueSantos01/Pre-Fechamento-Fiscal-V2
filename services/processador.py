import pandas as pd

from configs.unidades import UNIDADES

from schemas.colunas import validar_colunas

from utils.formatacao import (
    formatar_chaves,
    formatar_cfop
)

# =====================================================
# VALIDAÇÕES GERAIS
# =====================================================

from validacoes.chaves import validar_chaves
from validacoes.icms import calcular_icms
from validacoes.sequencia import validar_sequencia

from validacoes.nf_cancelada import (
    validar_retorno_sefaz,
    validar_data_cancelamento,
    validar_observacao_nf_cancelada
)

from validacoes.especies import (
    validar_especie_cfop,
    validar_nfcom_chave
)

from validacoes.cst import validar_cfop_cst


# =====================================================
# VALIDAÇÕES CFOP
# =====================================================

from validacoes.cfop import (

    validar_cfop_2556_icms_st,
    validar_cfop_1556_icms_st,

    validar_cfop_1556_icms,

    validar_cfop_1407_icms_com,
    validar_cfop_2407_icms_com,

    validar_cfop_1407_icms,
    validar_cfop_2407_icms,

    validar_cfop_2556_Vlr_ICMS_Com,
    validar_cfop_2551_Vlr_ICMS_Com,

    validar_cfop_2352_frete,

    validar_cfop_5556_ICMS,
    validar_cfop_6556_ICMS,

    validar_cfop_5556_DIFAL_ICMS,
    validar_cfop_6556_DIFAL_ICMS,

    validar_cfop_6107_icms,
    validar_cfop_6108_icms

)


# =====================================================
# ICMS COMPLEMENTAR
# =====================================================

from validacoes.icms_complementar import calcular_icms_complementar


# =====================================================
# DIFERENÇAS
# =====================================================

from calculos.diferencas import calcular_diferencas


# =====================================================
# CONVERSÃO SEGURA DE VALORES
# =====================================================

def converter_numero(valor):

    if pd.isna(valor):
        return 0

    if isinstance(valor, (int, float)):
        return valor

    valor = str(valor).strip()

    if valor == "":
        return 0

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


# =====================================================
# TRATAMENTO DE VALORES
# =====================================================

def ajustar_valores(df):

    colunas_valores = [

        "Vlr Contabil",
        "Base Icms",
        "Vlr. ICMS",
        "Vlr ICMS Com",
        "Icms Ret",
        "Difal ICMS",

        "Valor",
        "Valor Total",
        "Valor Nota",
        "Vlr Total",
        "Vlr Nota",
        "Total NF"

    ]

    for coluna in colunas_valores:

        if coluna in df.columns:

            df[coluna] = (
                df[coluna]
                .apply(converter_numero)
            )

    return df


# =====================================================
# PROCESSAMENTO PRINCIPAL
# =====================================================

def processar_planilha(arquivo):

    df = pd.read_excel(

        arquivo,

        dtype={
            "Chave Doc": str,
            "CFOP": str
        }

    )

    # ==========================================
    # Ajusta valores monetários
    # ==========================================

    df = ajustar_valores(df)

    # ==========================================
    # Observações
    # ==========================================

    if "Observacoes" not in df.columns:

        df["Observacoes"] = ""

    df["Observacoes"] = (

        df["Observacoes"]
        .fillna("")
        .astype(str)

    )

    # ==========================================
    # Validação das colunas
    # ==========================================

    validar_colunas(df)

    # ==========================================
    # Identifica a filial
    # ==========================================

    filial = int(df["Filial"].iloc[0])

    if filial not in UNIDADES:

        raise Exception(
            f"Filial {filial} não cadastrada"
        )

    dados_unidade = UNIDADES[filial]

    # ==========================================
    # Formatações
    # ==========================================

    df = formatar_chaves(df)

    df = formatar_cfop(df)

    # ==========================================
    # VALIDAÇÕES CFOP
    # ==========================================

    VALIDACOES_CFOP = [

        validar_cfop_2556_icms_st,
        validar_cfop_1556_icms_st,

        validar_cfop_1556_icms,

        validar_cfop_1407_icms_com,
        validar_cfop_2407_icms_com,

        validar_cfop_1407_icms,
        validar_cfop_2407_icms,

        validar_cfop_2556_Vlr_ICMS_Com,
        validar_cfop_2551_Vlr_ICMS_Com,

        validar_cfop_2352_frete,

        validar_cfop_5556_ICMS,
        validar_cfop_6556_ICMS,

        validar_cfop_5556_DIFAL_ICMS,
        validar_cfop_6556_DIFAL_ICMS,

        validar_cfop_6107_icms,
        validar_cfop_6108_icms

    ]

    for validacao in VALIDACOES_CFOP:

        df = validacao(df)

    # ==========================================
    # ICMS Complementar
    # ==========================================

    df = calcular_icms_complementar(
        df,
        dados_unidade
    )

    # ==========================================
    # ICMS Próprio
    # ==========================================

    df = calcular_icms(df)

    # ==========================================
    # Diferenças
    # ==========================================

    df = calcular_diferencas(df)

    # ==========================================
    # Validações Gerais
    # ==========================================

    VALIDACOES_GERAIS = [

        validar_chaves,

        validar_sequencia,

        validar_retorno_sefaz,
        validar_data_cancelamento,
        validar_observacao_nf_cancelada,

        validar_especie_cfop,
        validar_nfcom_chave,

        validar_cfop_cst

    ]

    for validacao in VALIDACOES_GERAIS:

        df = validacao(df)

    return df, dados_unidade
