import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = None


def digest_document(file, embeddings):
    global vectorstore
    file_path = f"./temp/{uploaded_file.name}"

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())

    loader = PyPDFLoader(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = loader.load_and_split(text_splitter)

    if embeddings == "openai":
        embedding_model = OpenAIEmbeddings(api_key=st.session_state.openai_api_key)

    vectorstore = FAISS.from_documents(docs, embedding_model)


# def search(query):
#     global vectorstore
#     retriever = vectorstore.as_retriever()
#     return retriever.invoke(query)


st.title("Búsqueda en PDF 🔎📄")

st.subheader("Cargar documento")
with st.form("digest_form"):
    col1, col2, col3 = st.columns(3)
    chunk_size = col1.number_input("Chunk size", value=1000)
    chunk_overlap = col2.number_input("Chunk overlap", value=200)
    embeddings = col3.selectbox(
        "Embeddings",
        ("openai", "huggingface"),
    )

    uploaded_file = st.file_uploader("Elegí un archivo .pdf", type="pdf")
    submitted = st.form_submit_button("Cargar", use_container_width=True)

    if submitted:
        digest_document(uploaded_file, embeddings)

    if vectorstore is not None:
        with st.expander(
            f"Documento almacenado en {vectorstore.index.ntotal} registros"
        ):
            with st.echo():
                st.write(vectorstore.docstore._dict)

st.subheader("Buscar")
with st.form("search_form"):
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    query = col1.text_input(
        "Ingrese el término de búsqueda:",
        disabled=not submitted,
    )
    submitted = col2.form_submit_button("Buscar", disabled=vectorstore is None)

    # if submitted:
    #     results = search(query)
    #     with st.echo():
    #         st.write(results)
