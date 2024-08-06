import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = (
        os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") != "" else ""
    )

pg = st.navigation([st.Page("home.py"), st.Page("retriever.py"), st.Page("pdf.py")])

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", type="password", value=st.session_state.openai_api_key
    )
    st.session_state.openai_api_key = openai_api_key

pg.run()
