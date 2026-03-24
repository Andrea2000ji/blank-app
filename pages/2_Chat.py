import streamlit as st
from core.claude_client import stream_response
from core.prompts import build_chat_system

st.set_page_config(page_title="Chat — ClarityDoc", page_icon="💬", layout="wide")
st.title("💬 Ask the Document")

if "doc_text" not in st.session_state:
    st.info("Upload a document from the sidebar to get started.")
    st.stop()

doc_text = st.session_state["doc_text"]
doc_name = st.session_state.get("doc_name", "Document")
st.caption(f"Chatting with: **{doc_name}**")

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

# Render history
for msg in st.session_state["chat_messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New question
if question := st.chat_input("Ask a question about the document…"):
    st.session_state["chat_messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    system = build_chat_system(doc_text)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state["chat_messages"]
    ]

    with st.chat_message("assistant"):
        answer = st.write_stream(stream_response(system, api_messages, max_tokens=2048))

    st.session_state["chat_messages"].append({"role": "assistant", "content": answer})
