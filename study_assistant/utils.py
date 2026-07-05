"""Small formatting utilities used by the application."""

from typing import Any


def message_content_to_text(content: Any) -> str:
    """Convert common LangChain message-content formats into plain text."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts: list[str] = []

        for item in content:
            if isinstance(item, str):
                text_parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    text_parts.append(text)

        if text_parts:
            return "\n".join(text_parts)

    return str(content)
