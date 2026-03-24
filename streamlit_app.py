import streamlit as st
from components.upload_widget import render_upload_widget

st.set_page_config(
    page_title="ClarityDoc",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔎 ClarityDoc")
    st.caption("AI-powered document intelligence")
    st.divider()

    # API key input
    api_key_input = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-…",
        help="Your key is stored only in session memory and never sent anywhere except the Anthropic API.",
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input

    st.divider()

    # Document upload
    st.subheader("Document")
    render_upload_widget()

    if "doc_name" in st.session_state:
        st.caption(f"**{st.session_state['doc_name']}**")
        st.caption(f"{st.session_state.get('doc_words', 0):,} words")

# ── Landing page ─────────────────────────────────────────────────────────────
st.title("Welcome to ClarityDoc")
st.write("Upload a document in the sidebar to unlock all features.")

features = [
    ("📝", "Summary", "Generate a concise executive summary in seconds."),
    ("💬", "Chat", "Ask any question about the document in natural language."),
    ("🔍", "Insights", "Extract action items, decisions, risks, and entities."),
    ("✏️", "Rewrite", "Transform any passage into a different style or tone."),
]

cols = st.columns(4)
for col, (icon, name, desc) in zip(cols, features):
    with col:
        st.markdown(
            f"""
            <div style="border:1px solid #e0e0e0; border-radius:12px; padding:20px; text-align:center; height:160px;">
                <div style="font-size:2rem">{icon}</div>
                <strong>{name}</strong>
                <p style="font-size:0.85rem; color:#666; margin-top:8px">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()
st.caption(
    "Powered by [Claude Opus 4.6](https://anthropic.com) · "
    "Supports PDF, TXT, and Markdown · "
    "Documents up to 100,000 characters"
)
