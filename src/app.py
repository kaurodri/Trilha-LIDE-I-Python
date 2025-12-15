import os
import streamlit as st
from downloader import baixar_audio_ytdlp
from transcriber import transcrever_audio
from use_relatorio import gerar_relatorio_gpt

# -----------------------------
# STREAMLIT APP
# -----------------------------
def main():
    base_path = os.path.dirname(__file__)
    logo_path = os.path.join(base_path, "assets", "logo.png")
    icon_path = os.path.join(base_path, "assets", "lide-icon.png")

    st.set_page_config(
        page_title="Extrator de Dados LIDE",
        page_icon=icon_path,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Estilo visual
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Roboto', sans-serif; }
        .stApp { background-color: #f0f9f7; }
        .titulo-principal { text-align: center; color: #0b6e3f !important; font-size: 2.8em; margin-bottom: 0.5em; }
        .stMarkdown h3 { color: #1fa772; text-align: center; }
        form { display: flex; flex-direction: column; align-items: center; }
        input[type="text"] { width: 400px !important; max-width: 90%; border-radius: 6px; padding: 0.5em; text-align: left !important; font-family: 'Roboto', sans-serif; }
        .stButton>button { background-color: #1fa772; color: white; border: none; padding: 0.6em 1.2em; font-size: 1em; border-radius: 8px; transition: background-color 0.3s ease; margin-top: 10px; font-family: 'Roboto', sans-serif; }
        .stButton>button:hover { background-color: #0ca35b; cursor: pointer; }
        </style>
    """, unsafe_allow_html=True)

    # Layout com logo e título
    col_logo, col_title, col_space = st.columns([1.5, 5.5, 1])
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=400)
    with col_title:
        st.markdown('<h1 class="titulo-principal">Extrator de Dados da LIDE</h1>', unsafe_allow_html=True)
    st.markdown("### Extrator de dados de vídeos")

    # Formulário
    with st.form("link_form"):
        link = st.text_input("Insira seu link aqui:", placeholder="Insira um link", key="link_input")
        submitted = st.form_submit_button("Enviar")

        if submitted:
            if link.strip() == "":
                st.warning("⚠ Por favor, insira um link válido!")
            else:
                st.success(f"✅ Link recebido: {link}")

                with st.spinner("⏳ Processando áudio..."):
                    caminho_audio = baixar_audio_ytdlp(link)

                    if caminho_audio:
                        texto_transcrito = transcrever_audio(caminho_audio)

                        st.info("📝 Gerando relatório com GPT...")
                        relatorio = gerar_relatorio_gpt(texto_transcrito)

                        st.subheader("Relatório gerado")
                        st.write(relatorio)
                    else:
                        st.error("Falha ao processar áudio do link. Verifique o link e tente novamente.")

if __name__ == "__main__":
    main()
