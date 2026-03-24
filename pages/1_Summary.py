import streamlit as st
from core.claude_client import stream_response
from core.prompts import build_summary_prompt

st.set_page_config(page_title="Summary — ClarityDoc", page_icon="📝", layout="wide")
st.title("📝 Document Summary")

if "doc_text" not in st.session_state:
    st.info("Upload a document from the sidebar to get started.")
    st.stop()

doc_text = st.session_state["doc_text"]
doc_name = st.session_state.get("doc_name", "Document")

st.caption(f"Summarizing: **{doc_name}** · {st.session_state.get('doc_words', 0):,} words")

length = st.radio(
    "Summary length",
    ["Brief (3 sentences)", "Standard (1 paragraph)", "Detailed (5+ paragraphs)"],
    horizontal=True,
)

if st.button("Generate Summary", type="primary"):
    system, user_msg = build_summary_prompt(doc_text, length)
    with st.spinner("Generating…"):
        result = st.write_stream(
            stream_response(system, [{"role": "user", "content": user_msg}])
        )
    st.session_state["summary"] = result
elif "summary" in st.session_state:
    st.markdown(st.session_state["summary"])
