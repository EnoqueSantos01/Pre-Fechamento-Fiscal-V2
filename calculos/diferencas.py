import pandas as pd


def calcular_diferencas(df):

    df = df.copy()

    # Cria as colunas
    if "Diferença ICMS Próprio" not in df.columns:
        df["Diferença ICMS Próprio"] = 0.0

    if "Diferença ICMS Complementar" not in df.columns:
        df["Diferença ICMS Complementar"] = 0.0

    # -------------------------
    # ICMS Próprio
    # -------------------------

    df["Vlr. ICMS"] = pd.to_numeric(
        df["Vlr. ICMS"],
        errors="coerce"
    ).fillna(0)

    df["ICMS Calculado"] = pd.to_numeric(
        df["ICMS Calculado"],
        errors="coerce"
    ).fillna(0)

    df["Diferença ICMS Próprio"] = (
        df["Vlr. ICMS"] -
        df["ICMS Calculado"]
    ).round(2)

    # -------------------------
    # ICMS Complementar
    # -------------------------

    df["Vlr ICMS Com"] = pd.to_numeric(
        df["Vlr ICMS Com"],
        errors="coerce"
    ).fillna(0)

    df["ICMS Complementar"] = pd.to_numeric(
        df["ICMS Complementar"],
        errors="coerce"
    ).fillna(0)

    df["Diferença ICMS Complementar"] = (
        df["Vlr ICMS Com"] -
        df["ICMS Complementar"]
    ).round(2)

    return df