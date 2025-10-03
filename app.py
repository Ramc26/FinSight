# app.py
import streamlit as st
from pathlib import Path
import pymupdf

from config import Config
from main import FinSight

def display_file_tree(root_dir):
    if not root_dir.exists():
        st.sidebar.warning("Extraction directory not found.")
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Extracted Files")
    
    for item in sorted(root_dir.iterdir()):
        if item.is_dir():
            with st.sidebar.expander(f"📁 {item.name}", expanded=False):
                for sub_item in sorted(item.rglob('*')):
                    if sub_item.is_file():
                        st.markdown(f"📄 {sub_item.name}")

def reset_session():
    st.session_state.clear()
    st.rerun()

st.set_page_config(page_title="FinSight", page_icon="🧠", layout="centered")

# --- Initialization ---
if 'finsight' not in st.session_state:
    st.session_state.finsight = FinSight()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'temp_pdf_path' not in st.session_state:
    st.session_state.temp_pdf_path = None
if 'password_required' not in st.session_state:
    st.session_state.password_required = False

with st.sidebar:
    st.title("FinSight Assistant")
    st.markdown("Your intelligent document analysis tool.")
    
    if st.session_state.pdf_processed:
        if st.button("Process New Document"):
            reset_session()
            
    display_file_tree(Config.EXTRACTIONS_DIR)

    # --- Developer Info Block ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("About the Developer")
    st.sidebar.markdown(
        """
        **Ram Bikkina** 🦉

        [Portfolio](https://ramc26.github.io/)

        *Open for Colab and Freelance*
        """
    )

st.title("🧠 FinSight")
st.subheader("Your intelligent document analysis tool.")
# --- PDF Upload and Processing Logic ---
if not st.session_state.pdf_processed:
    st.markdown("Upload a PDF document to begin the analysis.")
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type="pdf", 
        key="file_uploader"
    )

    if uploaded_file and not st.session_state.temp_pdf_path:
        temp_dir = Config.BASE_DIR / "temp"
        temp_dir.mkdir(exist_ok=True)
        st.session_state.temp_pdf_path = temp_dir / uploaded_file.name
        
        with open(st.session_state.temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        try:
            doc = pymupdf.open(st.session_state.temp_pdf_path)
            if doc.needs_pass:
                st.session_state.password_required = True
            doc.close()
        except Exception as e:
            st.error(f"Could not read the PDF. It may be corrupted. Error: {e}")
            reset_session()
        st.rerun()

    if st.session_state.password_required:
        st.warning("🔒 This PDF is password-protected.")
        password = st.text_input("Please enter the password:", type="password")
        if st.button("Unlock and Process"):
            if password:
                with st.spinner("Processing with password..."):
                    extraction_path = st.session_state.finsight.extract_pdf(
                        str(st.session_state.temp_pdf_path), 
                        password=password
                    )
                if extraction_path:
                    st.session_state.pdf_processed = True
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": "✅ Successfully processed the document. How can I help?"
                    })
                    st.session_state.temp_pdf_path.unlink()
                    st.session_state.password_required = False
                    st.session_state.temp_pdf_path = None
                    st.rerun()
                else:
                    st.error("Incorrect password or failed to process the PDF.")
            else:
                st.warning("Please enter a password.")

    elif st.session_state.temp_pdf_path and not st.session_state.password_required:
        with st.spinner("Extracting data..."):
            extraction_path = st.session_state.finsight.extract_pdf(str(st.session_state.temp_pdf_path))
        if extraction_path:
            st.session_state.pdf_processed = True
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "✅ Successfully processed the document. How can I help?"
            })
            st.session_state.temp_pdf_path.unlink()
            st.session_state.temp_pdf_path = None
            st.rerun()
        else:
            st.error("Failed to process the PDF.")
            reset_session()

# --- Chat Interface ---
if st.session_state.pdf_processed:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.button("Run Comprehensive Analysis"):
        st.session_state.messages.append({"role": "user", "content": "Run a comprehensive analysis."})
        with st.chat_message("user"):
            st.markdown("Run a comprehensive analysis.")
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = st.session_state.finsight.analyze_document(st.session_state.extraction_path)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.finsight.ask_question(prompt, st.session_state.extraction_path)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()