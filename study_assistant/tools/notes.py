"""LangChain tools for saving and retrieving study notes."""

from langchain.tools import tool

from study_assistant.storage import load_notes, write_notes


@tool
def save_study_note(topic: str, note: str) -> str:
    """
    Save a study note under a topic.

    Use this tool when the student asks to save, record, remember,
    or store information for later.
    """
    topic = topic.strip()
    note = note.strip()

    if not topic:
        return "A topic is required before a note can be saved."

    if not note:
        return "The note is empty, so nothing was saved."

    notes = load_notes()
    topic_key = topic.lower()

    notes.setdefault(topic_key, []).append(note)
    write_notes(notes)

    return f"Saved the note under the topic '{topic}'."


@tool
def read_study_notes(topic: str) -> str:
    """
    Retrieve saved study notes for a topic.

    Use this tool when the student asks to review, show, or retrieve
    notes that were saved earlier.
    """
    topic = topic.strip()

    if not topic:
        return "Please provide the topic whose notes should be retrieved."

    notes = load_notes()
    saved_notes = notes.get(topic.lower())

    if not saved_notes:
        return f"No saved notes were found for '{topic}'."

    return "\n".join(
        f"{number}. {note}"
        for number, note in enumerate(saved_notes, start=1)
    )


@tool
def list_study_topics() -> str:
    """
    List all topics that currently have saved study notes.

    Use this tool when the student asks what topics or notes have
    previously been saved.
    """
    notes = load_notes()

    if not notes:
        return "There are no saved study-note topics yet."

    return "\n".join(
        f"{number}. {topic}"
        for number, topic in enumerate(sorted(notes), start=1)
    )
