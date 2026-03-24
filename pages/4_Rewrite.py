import streamlit as st
from core.claude_client import stream_response
from core.prompts import build_rewrite_prompt

st.set_page_config(page_title="Rewrite — ClarityDoc", page_icon="✏️", layout="wide")
st.title("✏️ Rewrite Assistant")

if "doc_text" not in st.session_state:
    st.info("Upload a document from the sidebar to get started.")
    st.stop()

doc_text = st.session_state["doc_text"]

TONES = ["Formal", "Simplified", "Bullet Points", "Executive"]

col_input, col_output = st.columns(2)

with col_input:
    st.subheader("Original passage")
    if st.button("Use document opening", help="Pre-fill with the first 500 characters"):
        st.session_state["rewrite_input"] = doc_text[:500]

    passage = st.text_area(
        "Paste or type the text you want rewritten",
        value=st.session_state.get("rewrite_input", ""),
        height=300,
        label_visibility="collapsed",
        key="rewrite_input",
    )

    st.subheader("Target tone")
    cols = st.columns(len(TONES))
    selected_tone = st.session_state.get("selected_tone", TONES[0])
    for i, tone in enumerate(TONES):
        with cols[i]:
            if st.button(tone, use_container_width=True, type="primary" if tone == selected_tone else "secondary"):
                st.session_state["selected_tone"] = tone
                st.rerun()

with col_output:
    st.subheader("Rewritten version")
    if st.button("Rewrite", type="primary", disabled=not passage.strip()):
        tone = st.session_state.get("selected_tone", TONES[0])
        system, user_msg = build_rewrite_prompt(passage, tone)
        result = st.write_stream(
            stream_response(system, [{"role": "user", "content": user_msg}], max_tokens=2048)
        )
        st.session_state["rewrite_result"] = result
    elif "rewrite_result" in st.session_state:
        st.markdown(st.session_state["rewrite_result"])
