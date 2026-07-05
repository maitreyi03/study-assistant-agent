# Personal Study Assistant Agent

A beginner-friendly AI agent built with **LangChain** and a Groq-hosted external LLM. The code is separated into focused modules so each part of the agent is easier to understand, test, and extend.

## Project structure

```text
study-assistant-agent-refactored/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── study_notes.json
├── setup_mac_linux.sh
├── setup_windows.bat
└── study_assistant/
    ├── __init__.py
    ├── agent.py
    ├── cli.py
    ├── config.py
    ├── prompts.py
    ├── storage.py
    ├── utils.py
    └── tools/
        ├── __init__.py
        ├── calculator.py
        └── notes.py
```

## What each file does

| File | Responsibility |
|---|---|
| `app.py` | Small application entry point |
| `study_assistant/config.py` | Paths, model settings, thread ID, and `.env` loading |
| `study_assistant/storage.py` | Reads and writes `study_notes.json` |
| `study_assistant/prompts.py` | Stores the agent's system prompt |
| `study_assistant/tools/notes.py` | Save, read, and list-notes tools |
| `study_assistant/tools/calculator.py` | Restricted arithmetic calculator tool |
| `study_assistant/tools/__init__.py` | Collects the tools supplied to the agent |
| `study_assistant/agent.py` | Creates the Groq model, memory, and LangChain agent |
| `study_assistant/utils.py` | Converts model message content into printable text |
| `study_assistant/cli.py` | Runs the interactive terminal loop |

## Program flow

```text
app.py
  -> cli.main()
      -> create_study_agent()
          -> load configuration
          -> create Groq LLM
          -> register tools
          -> attach conversation memory
      -> read user messages
      -> invoke the agent
      -> print the final response
```

## Setup

Create a Groq API key and place it in a local `.env` file:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

### macOS or Linux

```bash
chmod +x setup_mac_linux.sh
./setup_mac_linux.sh
source .venv/bin/activate
python app.py
```

### Windows

```bat
setup_windows.bat
.venv\Scripts\activate
python app.py
```

## Why split the code?

The original `app.py` handled configuration, storage, tools, agent construction, output formatting, and the terminal interface. Separating these concerns makes the project easier to:

- Read and explain
- Debug
- Test
- Add new tools
- Replace the terminal with Streamlit later
- Replace JSON storage with SQLite later
- Change the model without changing unrelated code

## Adding another tool

Create a new file under `study_assistant/tools/`, define a function with LangChain's `@tool` decorator, and add it to `AGENT_TOOLS` in `study_assistant/tools/__init__.py`.

Example:

```python
from langchain.tools import tool


@tool
def word_counter(text: str) -> str:
    """Count the words in a block of text."""
    return str(len(text.split()))
```

Then import it and add it to the list:

```python
from study_assistant.tools.word_counter import word_counter

AGENT_TOOLS = [
    save_study_note,
    read_study_notes,
    list_study_topics,
    calculator,
    word_counter,
]
```
