from io import BytesIO
import streamlit as st

MAX_CHARS = 100_000


def extract_text(uploaded_file) -> str:
    """Extract plain text from an uploaded PDF or text file."""
    file_type = uploaded_file.type
    raw = uploaded_file.read()

    if file_type == "application/pdf":
        text = _extract_pdf(raw)
    else:
        text = raw.decode("utf-8", errors="replace")

    if len(text) > MAX_CHARS:
        st.warning(
            f"Document truncated to {MAX_CHARS:,} characters "
            f"(original: {len(text):,}). Results may be incomplete."
        )
        text = text[:MAX_CHARS]

    return text


def _extract_pdf(raw: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(raw))
    pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages.append(page_text)
    return "\n\n".join(pages)


def word_count(text: str) -> int:
    return len(text.split())
