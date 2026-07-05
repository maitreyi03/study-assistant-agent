import ast
import json
import operator
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver


# ---------------------------------------------------------
# Project configuration
# ---------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
NOTES_FILE = PROJECT_DIR / "study_notes.json"

load_dotenv(PROJECT_DIR / ".env")

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "\nMissing GROQ_API_KEY.\n\n"
        "1. Copy .env.example to a new file named .env\n"
        "2. Open .env and replace the placeholder with your Groq API key\n"
        "3. Run the application again\n"
    )


# ---------------------------------------------------------
# Local study-note storage
# ---------------------------------------------------------

def load_notes() -> dict[str, list[str]]:
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

    cleaned_notes: dict[str, list[str]] = {}

    for topic, topic_notes in data.items():
        if isinstance(topic, str) and isinstance(topic_notes, list):
            cleaned_notes[topic] = [
                str(note) for note in topic_notes
                if isinstance(note, (str, int, float))
            ]

    return cleaned_notes


def write_notes(notes: dict[str, list[str]]) -> None:
    """Save all study notes to the local JSON file."""
    with NOTES_FILE.open("w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2, ensure_ascii=False)


# ---------------------------------------------------------
# Agent tools
# ---------------------------------------------------------

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
    topic_key = topic.lower()
    saved_notes = notes.get(topic_key)

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

    topics = sorted(notes.keys())
    return "\n".join(
        f"{number}. {topic}"
        for number, topic in enumerate(topics, start=1)
    )


# Only these arithmetic operations are permitted.
ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY_OPERATORS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_math_node(node: ast.AST) -> int | float:
    """Recursively evaluate a restricted mathematical expression."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise ValueError("Boolean values are not supported.")

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are supported.")

    if isinstance(node, ast.BinOp):
        operation = ALLOWED_BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("That mathematical operation is not supported.")

        left = evaluate_math_node(node.left)
        right = evaluate_math_node(node.right)

        # Prevent accidentally requesting an extremely large calculation.
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("The exponent is too large.")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = ALLOWED_UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("That unary operation is not supported.")

        return operation(evaluate_math_node(node.operand))

    raise ValueError("The expression contains unsupported content.")


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Examples:
    - 25 * 4
    - (10 + 5) / 3
    - 2 ** 8
    """
    try:
        parsed_expression = ast.parse(expression, mode="eval")
        answer = evaluate_math_node(parsed_expression.body)
        return str(answer)
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as error:
        return f"Could not calculate the expression: {error}"


# ---------------------------------------------------------
# External LLM and LangChain agent
# ---------------------------------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)

memory = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[
        save_study_note,
        read_study_notes,
        list_study_topics,
        calculator,
    ],
    system_prompt="""
You are a helpful personal study assistant.

Your responsibilities are to:
1. Explain difficult concepts in clear, beginner-friendly language.
2. Provide examples when they improve understanding.
3. Create quizzes, flashcards, practice problems, and study plans.
4. Use the calculator tool for arithmetic instead of calculating silently.
5. Save information when the student asks you to remember or record a note.
6. Retrieve saved notes when requested.
7. List saved study topics when requested.

Do not claim that a note was saved unless the save_study_note tool
successfully returned a confirmation.

When explaining a concept, use this structure when appropriate:
- Simple explanation
- Important details
- Example
- Quick knowledge check

Keep responses focused and adapt the level of detail to the student's request.
""",
    checkpointer=memory,
)


# ---------------------------------------------------------
# Output formatting
# ---------------------------------------------------------

def message_content_to_text(content: Any) -> str:
    """Convert common LangChain message-content formats into text."""
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


# ---------------------------------------------------------
# Command-line application
# ---------------------------------------------------------

def main() -> None:
    print("=" * 64)
    print("Personal Study Assistant")
    print("Powered by LangChain and Groq")
    print("Enter 'exit' or 'quit' to close the program.")
    print("=" * 64)

    # Messages using the same thread ID share in-memory conversation context.
    # This memory lasts only until the application is closed.
    config = {
        "configurable": {
            "thread_id": "student-session-1",
        }
    }

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("\nStudy Assistant: Good luck with your studies!")
                break

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                },
                config=config,
            )

            final_message = result["messages"][-1]
            response_text = message_content_to_text(final_message.content)

            print(f"\nStudy Assistant: {response_text}")

        except KeyboardInterrupt:
            print("\n\nStudy Assistant: Session ended.")
            break

        except Exception as error:
            print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    main()
