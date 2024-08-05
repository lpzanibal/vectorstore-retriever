import streamlit as st


def get_results(input_text):
    st.info("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")


st.title("Vectorstore Retriever 🔎📚")

with st.form("search_form"):
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    text = col1.text_input("Ingrese el término de búsqueda:")
    submitted = col2.form_submit_button("Buscar", use_container_width=True)

    st.text("Resultados:")
    if submitted:
        get_results(text)
