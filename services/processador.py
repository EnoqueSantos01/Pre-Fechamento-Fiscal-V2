import pandas as pd

from configs.unidades import UNIDADES

from schemas.colunas import validar_colunas

from utils.formatacao import (
    formatar_chaves,
    formatar_cfop
)


# VALIDAÇÕES GERAIS
from validacoes.chaves import validar_chaves
from validacoes.icms import calcular_icms
from validacoes.sequencia import validar_sequencia


# VALIDAÇÕES CFOP
from validacoes.cfop import (
    validar_cfop_2556_icms_st,
    validar_cfop_1556_icms_st,
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


# ICMS COMPLEMENTAR
from validacoes.icms_complementar import calcular_icms_complementar


# DIFERENÇAS
from calculos.diferencas import calcular_diferencas



# =====================================================
# TRATAMENTO DE VALORES MONETÁRIOS
# =====================================================

def ajustar_valores_monetarios(df):

    palavras_valores = [
        "valor",
        "vlr",
        "base",
        "icms",
        "ipi",
        "pis",
        "cofins",
        "total",
        "contabil"
    ]


    for coluna in df.columns:

        nome_coluna = coluna.lower()


        if any(
            palavra in nome_coluna
            for palavra in palavras_valores
        ):


            def converter(valor):

                if pd.isna(valor):
                    return 0


                # Se já veio como número do Excel
                if isinstance(valor, (int, float)):
                    return valor


                valor = str(valor).strip()


                if valor == "":
                    return 0


                valor = (
                    valor
                    .replace("R$", "")
                    .strip()
                )


                # Caso venha como texto brasileiro
                # Exemplo: 1.786,35
                if "," in valor:

                    valor = (
                        valor
                        .replace(".", "")
                        .replace(",", ".")
                    )


                try:
                    return float(valor)

                except:
                    return valor


            df[coluna] = df[coluna].apply(
                converter
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


    # Ajusta valores monetários
    df = ajustar_valores_monetarios(df)



    # OBSERVAÇÕES

    if "Observacoes" not in df.columns:

        df["Observacoes"] = ""


    df["Observacoes"] = (
        df["Observacoes"]
        .fillna("")
        .astype(str)
    )



    # VALIDA COLUNAS

    validar_colunas(df)



    # IDENTIFICA FILIAL

    filial = int(
        df["Filial"].iloc[0]
    )


    if filial not in UNIDADES:

        raise Exception(
            f"Filial {filial} não cadastrada"
        )


    dados_unidade = UNIDADES[filial]



    # FORMATAÇÕES

    df = formatar_chaves(df)

    df = formatar_cfop(df)



    # =================================================
    # VALIDAÇÕES CFOP
    # =================================================

    VALIDACOES_CFOP = [

        validar_cfop_2556_icms_st,
        validar_cfop_1556_icms_st,

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



    # =================================================
    # ICMS COMPLEMENTAR
    # =================================================

    df = calcular_icms_complementar(
        df,
        dados_unidade
    )



    # =================================================
    # CÁLCULOS
    # =================================================

    df = calcular_icms(df)


    df = calcular_icms_complementar(
        df,
        dados_unidade
    )


    df = calcular_diferencas(df)



    # =================================================
    # VALIDAÇÕES GERAIS
    # =================================================

    VALIDACOES_GERAIS = [

        validar_chaves,
        validar_sequencia

    ]


    for validacao in VALIDACOES_GERAIS:

        df = validacao(df)



    return df, dados_unidade
