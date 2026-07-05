"""Functions for reading and writing study notes."""

import json

from study_assistant.config import NOTES_FILE


NotesDictionary = dict[str, list[str]]


def load_notes() -> NotesDictionary:
    """Load study notes from the local JSON file."""
    if not NOTES_FILE.exists():
        return {}

    try:
        with NOTES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

    if not isinstance(data, dict):
        return {}

    cleaned_notes: NotesDictionary = {}

    for topic, topic_notes in data.items():
        if isinstance(topic, str) and isinstance(topic_notes, list):
            cleaned_notes[topic] = [
                str(note)
                for note in topic_notes
                if isinstance(note, (str, int, float))
            ]

    return cleaned_notes


def write_notes(notes: NotesDictionary) -> None:
    """Write all study notes to the local JSON file."""
    with NOTES_FILE.open("w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2, ensure_ascii=False)
