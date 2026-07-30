import pandas as pd

from configs.unidades import UNIDADES

from schemas.colunas import validar_colunas

from utils.formatacao import (
    formatar_chaves,
    formatar_cfop
)

# ===========================
# VALIDAÇÕES GERAIS
# ===========================

from validacoes.chaves import validar_chaves
from validacoes.nf_cancelada import validar_nf_cancelada
from validacoes.especies import (
    validar_especie_cfop,
    validar_nfcom_chave
)
from validacoes.cst import validar_cfop_cst

# ===========================
# ICMS
# ===========================

from validacoes.icms import calcular_icms
from validacoes.icms_complementar import calcular_icms_complementar

# ===========================
# DIFERENÇAS
# ===========================

from calculos.diferencas import calcular_diferencas

# ===========================
# VALIDAÇÕES CFOP
# ===========================

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
# CONVERSÃO SEGURA
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
# AJUSTA COLUNAS NUMÉRICAS
# =====================================================

def ajustar_valores(df):

    colunas = [

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

    for coluna in colunas:

        if coluna in df.columns:

            df[coluna] = df[coluna].apply(
                converter_numero
            )

    return df


# =====================================================
# PROCESSAMENTO
# =====================================================

def processar_planilha(arquivo):

    df = pd.read_excel(

        arquivo,

        dtype={

            "Chave Doc": str,
            "CFOP": str

        }

    )

    # Ajusta valores

    df = ajustar_valores(df)

    # Observações

    if "Observacoes" not in df.columns:
        df["Observacoes"] = ""

    df["Observacoes"] = (
        df["Observacoes"]
        .fillna("")
        .astype(str)
    )

    # Validação estrutura

    validar_colunas(df)

    # Filial

    filial = int(df["Filial"].iloc[0])

    if filial not in UNIDADES:

        raise Exception(
            f"Filial {filial} não cadastrada."
        )

    dados_unidade = UNIDADES[filial]

    # Formatações

    df = formatar_chaves(df)
    df = formatar_cfop(df)

    # ====================================
    # CFOP
    # ====================================

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

    # ====================================
    # Cálculos
    # ====================================

    df = calcular_icms_complementar(
        df,
        dados_unidade
    )

    df = calcular_icms(df)

    df = calcular_diferencas(df)

    # ====================================
    # Validações gerais
    # ====================================

    VALIDACOES_GERAIS = [

        validar_chaves,

        validar_nf_cancelada,

        validar_especie_cfop,

        validar_nfcom_chave,

        validar_cfop_cst

    ]

    for validacao in VALIDACOES_GERAIS:

        df = validacao(df)

    return df, dados_unidade
