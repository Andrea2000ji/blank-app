import streamlit as st
from core.document_parser import extract_text, word_count


def render_upload_widget():
    """Render the file uploader and process the document into session state."""
    uploaded = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt", "md"],
        label_visibility="collapsed",
    )

    if uploaded is not None:
        current_name = st.session_state.get("doc_name")
        if current_name != uploaded.name:
            with st.spinner("Parsing document…"):
                text = extract_text(uploaded)
            st.session_state["doc_text"] = text
            st.session_state["doc_name"] = uploaded.name
            st.session_state["doc_words"] = word_count(text)
            # Clear stale results from a previous document
            st.session_state.pop("summary", None)
            st.session_state.pop("insights", None)
            st.session_state.pop("chat_messages", None)
            st.success(f"Loaded **{uploaded.name}**")
