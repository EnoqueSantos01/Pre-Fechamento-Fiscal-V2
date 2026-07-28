from utils.observacoes import adicionar_observacao



def validar_sequencia(df):

    if "NUMERO" not in df.columns:
        return df

    numeros = df["NUMERO"].fillna(0)

    filtro = numeros.ne(numeros.shift() + 1)

    filtro.iloc[0] = False

    return adicionar_observacao(
        df,
        filtro,
        "Quebra de sequência numérica"
    )