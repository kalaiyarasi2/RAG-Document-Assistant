# app.py
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables (for local dev)
load_dotenv()

# Set page config
st.set_page_config(
    page_title="📚 RAG Document Assistant",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 RAG Document Assistant")
st.markdown("Upload **PDF, DOCX, TXT, CSV, Excel, PPTX** and ask questions using **Llama3-8b-8192**.")

# === API Key Handling (Local + Cloud Safe) ===
def get_api_key():
    # 1. Try Streamlit secrets (for Streamlit Cloud)
    try:
        return st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    # 2. Try .env file (for local)
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    # 3. Ask user to input
    st.warning("🔑 Groq API key is required.")
    st.markdown("Get a free key at [Groq Console](https://console.groq.com/keys)")
    return st.text_input("Enter your Groq API Key:", type="password")

api_key = get_api_key()
if not api_key:
    st.stop()

# === Import After Key is Available ===
try:
    from backend import RAGSystem
except ModuleNotFoundError as e:
    st.error(f"❌ Missing module: {e}. Did you install requirements?")
    st.code("pip install -r requirements.txt")
    st.stop()

# === Initialize RAG System (Cached) ===
@st.cache_resource
def get_rag_system(api_key):
    try:
        return RAGSystem(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Failed to initialize RAG system: {e}")
        st.stop()

rag = get_rag_system(api_key)

# === File Upload Sidebar ===
st.sidebar.header("📁 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Drag & drop files here",
    type=["pdf", "docx", "txt", "csv", "xlsx", "pptx"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("🔄 Saving files..."):
        for file in uploaded_files:
            (Path("raw_docs") / file.name).write_bytes(file.read())
    st.sidebar.success(f"✅ {len(uploaded_files)} file(s) uploaded!")

# Rebuild index button
if st.sidebar.button("⚡ Rebuild Index"):
    st.cache_resource.clear()
    st.rerun()

# Build index if needed
if not hasattr(rag, 'index') or rag.index is None:
    with st.spinner("🔍 Building search index... (may take a moment)"):
        try:
            rag.build_or_load_index()
            st.session_state.index_built = True
        except Exception as e:
            st.error(f"❌ Index build failed: {e}")
else:
    st.session_state.index_built = True

# === Chat Interface ===
if st.session_state.get("index_built"):
    st.success("✅ Document index is ready! Ask anything below.")

    # Fixed model (only Llama3)
    model = "llama3-8b-8192"
    st.write("🧠 Using: **Llama3-8b-8192** (fast & reliable)")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if prompt := st.chat_input("Ask about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤔 Retrieving & generating..."):
                answer, context = rag.query(prompt, model=model)
                st.write(answer)
                with st.expander("📄 View retrieved context"):
                    st.text(context[:3000] + "..." if len(context) > 3000 else context)
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("📤 Upload documents to get started.")

# === Optional: View Processed Files ===
if st.sidebar.checkbox("📂 View Extracted Text"):
    txt_files = list(Path("processed").glob("*.txt"))
    if not txt_files:
        st.sidebar.info("No extracted text yet.")
    else:
        selected = st.sidebar.selectbox("Choose file:", txt_files, format_func=lambda x: x.name)
        st.sidebar.text_area("Content", selected.read_text(), height=300)