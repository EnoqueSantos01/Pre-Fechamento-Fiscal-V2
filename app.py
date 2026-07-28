import streamlit as st
import pandas as pd

from io import BytesIO
from datetime import datetime

from services.processador import processar_planilha

from database.auth import carregar_usuarios
from database.logs_manager import salvar_log


# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="Pré - Fechamento Fiscal",
    page_icon="🧾",
    layout="wide"
)


# ==============================
# USUÁRIOS
# ==============================

usuarios = carregar_usuarios()



# ==============================
# CONTROLE LOGIN
# ==============================

if "logado" not in st.session_state:

    st.session_state["logado"] = False



# ==============================
# LOGIN
# ==============================

if not st.session_state["logado"]:


    st.title("🔐 Login do Sistema Fiscal")


    usuario = st.text_input(
        "Usuário"
    )


    senha = st.text_input(
        "Senha",
        type="password"
    )



    if st.button("Entrar"):


        if (
            usuario in usuarios
            and usuarios[usuario]["senha"] == senha
        ):


            st.session_state["logado"] = True

            st.session_state["usuario"] = usuario

            st.session_state["nome"] = (
                usuarios[usuario]["nome"]
            )


            st.success(
                "Login realizado com sucesso"
            )


            st.rerun()


        else:

            st.error(
                "Usuário ou senha inválidos"
            )


    st.stop()



# ==============================
# SIDEBAR
# ==============================

with st.sidebar:


    try:

        st.image(
            "assets/logo.png",
            width=180
        )

    except:

        pass



    st.markdown("---")


    st.success(
        "Sistema Fiscal Inteligente"
    )


    st.markdown(
        """
        ### Módulos

        ✅ Pré Fechamento  
        ✅ Validações Fiscais  
        ✅ Conferência CFOP  
        ✅ ICMS  
        ✅ ICMS ST  
        """
    )


    st.markdown("---")


    st.success(
        f"Usuário logado: {st.session_state['nome']}"
    )



    if st.button("🚪 Sair do sistema"):


        st.session_state.clear()

        st.rerun()



# ==============================
# CABEÇALHO
# ==============================

col1, col2 = st.columns(
    [1, 3]
)



with col1:


    try:

        st.image(
            "assets/mascote.png",
            width=220
        )

    except:

        pass



with col2:


    st.title(
        "🧾 Pré - Fechamento Fiscal"
    )


    st.subheader(
        "Assistente Inteligente de Validação Fiscal"
    )


    st.info(
        "Importe a planilha para iniciar a análise automática"
    )



st.markdown("---")



# ==============================
# UPLOAD
# ==============================

arquivo = st.file_uploader(

    "📂 Importe a planilha Excel",

    type=["xlsx"]

)



# ==============================
# PROCESSAMENTO CONTROLADO
# ==============================

if arquivo:


    nome_arquivo = arquivo.name



    # Processa somente se for um novo arquivo

    if (
        "arquivo_processado" not in st.session_state
        or st.session_state["arquivo_processado"] != nome_arquivo
    ):


        try:


            with st.spinner(
                "🔎 Processando planilha..."
            ):


                df, unidade = processar_planilha(
                    arquivo
                )



            st.session_state["df_resultado"] = df

            st.session_state["unidade_resultado"] = unidade

            st.session_state["arquivo_processado"] = nome_arquivo



            # Salva log apenas uma vez

            salvar_log({

                "usuario":
                    st.session_state["usuario"],


                "nome":
                    st.session_state["nome"],


                "data_hora":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),


                "arquivo":
                    arquivo.name,


                "unidade":
                    unidade["nome"],


                "estado":
                    unidade["estado"],


                "linhas_processadas":
                    len(df)

            })


        except Exception as erro:


            st.error(
                f"Erro durante processamento: {erro}"
            )

            st.stop()



    # Recupera resultado salvo

    df = st.session_state["df_resultado"]

    unidade = st.session_state["unidade_resultado"]



    # ==============================
    # RESULTADO
    # ==============================

    st.success(
        "✅ Análise concluída com sucesso"
    )



    st.info(
        f"""
        Unidade identificada:

        **{unidade['nome']}**

        Estado:

        **{unidade['estado']}**
        """
    )



    st.subheader(
        "Resultado das validações"
    )



    st.dataframe(

        df,

        use_container_width=True,

        height=650

    )



    # ==============================
    # EXPORTAÇÃO EXCEL
    # ==============================

    output = BytesIO()



    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:


        df.to_excel(

            writer,

            index=False,

            sheet_name="Resultado"

        )



    st.download_button(

        label="📥 Baixar Resultado Excel",

        data=output.getvalue(),

        file_name="resultado_pre_fechamento.xlsx",

        mime=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        )

    )
