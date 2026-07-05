"""Tools available to the study assistant agent."""

from study_assistant.tools.calculator import calculator
from study_assistant.tools.notes import (
    list_study_topics,
    read_study_notes,
    save_study_note,
)


AGENT_TOOLS = [
    save_study_note,
    read_study_notes,
    list_study_topics,
    calculator,
]

__all__ = [
    "AGENT_TOOLS",
    "calculator",
    "list_study_topics",
    "read_study_notes",
    "save_study_note",
]
