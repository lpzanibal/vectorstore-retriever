import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def digest_document(file, openai_api_key):
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_file.getvalue())
        file_name = uploaded_file.name

    loader = PyPDFLoader(temp_file)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = loader.load_and_split(text_splitter)
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    db = FAISS.from_documents(docs, embeddings)
    st.text(db.index.ntotal)


st.title("Búsqueda en PDF")

with st.form("form"):
    openai_api_key = st.text_input(
        "OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    col1, col2 = st.columns(2)
    chunk_size = col1.number_input("Chunk size", value=1000)
    chunk_overlap = col2.number_input("Chunk overlap", value=200)

    uploaded_file = st.file_uploader('Elegí un archivo .pdf', type="pdf")

    submitted = col2.form_submit_button("Buscar", use_container_width=True)

    if submitted:
        digest_document(uploaded_file, openai_api_key)

question = st.text_input(
    "Ingrese el término de búsqueda:",
    disabled=not submitted,
)
