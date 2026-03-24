import os
import anthropic
import streamlit as st

MODEL = "claude-opus-4-6"


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client using the API key from session state, secrets, or env."""
    api_key = st.session_state.get("api_key") or _read_secret()
    if not api_key:
        st.error("No API key found. Enter your Anthropic API key in the sidebar.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


def _read_secret() -> str | None:
    try:
        return st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


def stream_response(system: str, messages: list, max_tokens: int = 4096):
    """
    Generator that yields text deltas from a streaming Claude response.
    Designed for use with st.write_stream().
    """
    client = get_client()
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
