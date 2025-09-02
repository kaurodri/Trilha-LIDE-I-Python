import streamlit as st
import streamlit.components.v1 as components
import requests

def main():
    st.set_page_config(
        page_title="LIDE FERRAMENTA",
        initial_sidebar_state="expanded",
        page_icon="⚙️",
        layout="centered",
    )

    col1, col2 = st.columns([1, 7])
    with col2:
        st.markdown('Ferramenta 1', unsafe_allow_html=True)
    with col1:
        st.markdown("LIDE", unsafe_allow_html=True)
    with st.form("link_form"):
        link = st.text_input("Insira seu link aqui:",
            placeholder="COLAR LINK AQUI",
            key="link_input")
        submitted = st.form_submit_button("Concluir")

if __name__ == "__main__":
    main()