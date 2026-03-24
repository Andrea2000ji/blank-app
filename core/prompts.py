def build_summary_prompt(doc_text: str, length: str) -> tuple[str, str]:
    length_map = {
        "Brief (3 sentences)": "Summarize the document in exactly 3 concise sentences.",
        "Standard (1 paragraph)": "Write a single well-structured paragraph summarizing the document.",
        "Detailed (5+ paragraphs)": (
            "Write a detailed summary in 5 or more paragraphs covering the main "
            "themes, key arguments, supporting evidence, and conclusions."
        ),
    }
    instruction = length_map.get(length, length_map["Standard (1 paragraph)"])
    system = (
        "You are an expert document analyst. "
        "Your task is to summarize documents accurately and concisely. "
        f"Here is the document to analyze:\n\n<document>\n{doc_text}\n</document>"
    )
    user = instruction
    return system, user


def build_chat_system(doc_text: str) -> str:
    return (
        "You are a helpful assistant that answers questions strictly based on the "
        "provided document. Do not use any external knowledge. If the answer cannot "
        "be found in the document, say so clearly.\n\n"
        f"<document>\n{doc_text}\n</document>"
    )


def build_insights_prompt(doc_text: str, mode: str) -> tuple[str, str]:
    mode_instructions = {
        "Action Items": (
            "Extract all action items, tasks, and to-dos from the document. "
            "Present them as a numbered list with the responsible party (if mentioned)."
        ),
        "Key Decisions": (
            "Identify all key decisions made or discussed in the document. "
            "For each, include what was decided and any relevant context."
        ),
        "Risks & Issues": (
            "Identify all risks, problems, concerns, or issues raised in the document. "
            "Rate each as High / Medium / Low if context allows."
        ),
        "Named Entities": (
            "Extract all important named entities: people, organizations, locations, "
            "dates, products, and technologies. Group them by category."
        ),
    }
    instruction = mode_instructions.get(mode, mode_instructions["Action Items"])
    system = (
        "You are an expert analyst. Extract structured insights from the document below. "
        "Be thorough and precise. Format your output clearly in Markdown.\n\n"
        f"<document>\n{doc_text}\n</document>"
    )
    return system, instruction


def build_rewrite_prompt(passage: str, tone: str) -> tuple[str, str]:
    tone_instructions = {
        "Formal": "Rewrite the passage in a professional, formal register suitable for business or academic contexts.",
        "Simplified": "Rewrite the passage in plain language that a non-expert can understand. Use short sentences and common words.",
        "Bullet Points": "Convert the passage into a clear, concise bulleted list that preserves all key information.",
        "Executive": "Rewrite the passage as a tight executive summary, focusing only on the most critical points and implications.",
    }
    instruction = tone_instructions.get(tone, tone_instructions["Formal"])
    system = (
        "You are a professional editor and writing expert. "
        "Your task is to rewrite passages according to specific style instructions. "
        "Preserve the original meaning while changing the style and format."
    )
    user = f"{instruction}\n\nOriginal passage:\n\n{passage}"
    return system, user
