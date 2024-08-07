import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = None

st.title("Búsqueda en PDF 🔎📄")

st.subheader("Cargar documento")
col1, col2, col3 = st.columns(3)
chunk_size = col1.number_input("Chunk size", value=1000)
chunk_overlap = col2.number_input("Chunk overlap", value=200)
embeddings = col3.selectbox(
    "Embeddings",
    ("openai", "huggingface"),
)
uploaded_file = st.file_uploader("Elegí un archivo .pdf", type="pdf")

if st.button("Cargar", use_container_width=True):
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

if vectorstore is not None:
    with st.expander(f"Documento almacenado en {vectorstore.index.ntotal} registros"):
        with st.echo():
            st.write(vectorstore.docstore._dict)

st.subheader("Buscar")
col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
search_type = col1.selectbox(
    "Tipo de búsqueda",
    ("similarity", "similarity_score_threshold", "mmr"),
)
# search_kwargs={"score_threshold": 0.5}
top_k = col2.number_input("Top k", value=4)
score_threshold = col3.number_input(
    "Score threshold", value=0.5, disabled=search_type != "similarity_score_threshold"
)
query = st.text_input(
    "Ingrese el término de búsqueda:",
    disabled=vectorstore is None,
)
if st.button("Buscar", use_container_width=True):
    search_kwargs = {"score_threshold": score_threshold, "k": top_k}
    retriever = vectorstore.as_retriever(
        search_type=search_type, search_kwargs=search_kwargs
    )
    results = retriever.invoke(query)
    with st.echo():
        st.write(results)
