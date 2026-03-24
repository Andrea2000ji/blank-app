import streamlit as st
from core.claude_client import stream_response
from core.prompts import build_insights_prompt

st.set_page_config(page_title="Insights — ClarityDoc", page_icon="🔍", layout="wide")
st.title("🔍 Key Insights")

if "doc_text" not in st.session_state:
    st.info("Upload a document from the sidebar to get started.")
    st.stop()

doc_text = st.session_state["doc_text"]
doc_name = st.session_state.get("doc_name", "Document")
st.caption(f"Analysing: **{doc_name}**")

MODES = ["Action Items", "Key Decisions", "Risks & Issues", "Named Entities"]

mode = st.selectbox("Insight type", MODES)

if "insights" not in st.session_state:
    st.session_state["insights"] = {}

if st.button("Extract Insights", type="primary"):
    system, user_msg = build_insights_prompt(doc_text, mode)
    with st.spinner("Extracting…"):
        result = st.write_stream(
            stream_response(system, [{"role": "user", "content": user_msg}])
        )
    st.session_state["insights"][mode] = result
elif mode in st.session_state.get("insights", {}):
    st.markdown(st.session_state["insights"][mode])
