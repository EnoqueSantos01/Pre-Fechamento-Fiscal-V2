from utils.observacoes import adicionar_observacao



def validar_chaves(df):

    filtro = df["Chave Doc"].astype(str).str.len() != 44

    return adicionar_observacao(
        df,
        filtro,
        "Chave inválida"
    )
