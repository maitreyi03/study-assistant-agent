# Personal Study Assistant Agent

A beginner-friendly AI agent built with **LangChain** and a free external LLM hosted by **Groq**.

The project is designed to help you learn how LangChain agents work by giving the language model access to tools such as a calculator and local study-note storage.

The project does **not** require Google Cloud, Vertex AI, or a paid cloud account.

---

## Project Overview

The Personal Study Assistant is a command-line application that can:

- Explain difficult concepts in simple language
- Create quizzes, flashcards, practice questions, and study plans
- Perform mathematical calculations
- Save study notes under different topics
- Retrieve previously saved notes
- List all topics that contain saved notes
- Remember the current conversation while the program is running

The application uses a Groq-hosted large language model as its reasoning engine and LangChain to connect the model to tools.

---

## What Is an AI Agent?

A normal chatbot receives a message and generates a response.

An **agent** can do more. It can examine the user's request, decide whether it needs a tool, run that tool, read the result, and then produce a final response.

For example:

```text
User: Explain gradient descent.
Agent: Answers directly using the LLM.

User: Calculate (25 * 8) / 4.
Agent: Calls the calculator tool and returns the result.

User: Remember that a Python dictionary stores key-value pairs.
Agent: Calls the save-study-note tool.

User: Show me my Python notes.
Agent: Calls the read-study-notes tool.
```

The language model chooses which action to take based on the user's message.

---

## Main Technologies

| Technology    | Purpose                                  |
| ------------- | ---------------------------------------- |
| Python        | Main programming language                |
| LangChain     | Creates and manages the AI agent         |
| LangGraph     | Provides the agent's conversation memory |
| Groq          | Hosts the external LLM                   |
| Llama 3.3     | Generates answers and selects tools      |
| python-dotenv | Loads the API key from `.env`            |
| JSON          | Stores study notes locally               |

---

## How the Project Works

```text
User runs: python app.py
          |
          v
app.py calls study_assistant.cli.main()
          |
          v
cli.py reads the user's terminal input
          |
          v
agent.py sends the message to the LangChain agent
          |
          v
Groq-hosted LLM decides what to do
          |
          +------------------------------+
          |                              |
          v                              v
Answer directly                    Call a tool
                                         |
                         +---------------+---------------+
                         |               |               |
                         v               v               v
                  calculator.py      notes.py        notes.py
                                     save/read       list topics
                                         |
                                         v
                                  storage.py reads or
                                  updates study_notes.json
                                         |
                                         v
                              Tool result returns to agent
                                         |
                                         v
                              utils.py formats the response
                                         |
                                         v
                                cli.py prints the answer
```

The modules work together as follows:

1. `app.py` starts the program.
2. `cli.py` manages the terminal conversation.
3. `agent.py` creates and invokes the LangChain agent.
4. `config.py` provides shared configuration and file paths.
5. `prompts.py` provides the system instructions.
6. `tools/` contains actions the language model can choose.
7. `storage.py` manages persistent note data.
8. `utils.py` prepares the final response for display.

## Agent Tools

The project gives the LLM access to four tools defined inside `study_assistant/tools/`.

### 1. `save_study_note`

Saves a note under a topic in `study_notes.json`.

Example request:

```text
Remember under machine learning that overfitting happens when a model
performs well on training data but poorly on new data.
```

Example stored data:

```json
{
  "machine learning": [
    "Overfitting happens when a model performs well on training data but poorly on new data."
  ]
}
```

### 2. `read_study_notes`

Retrieves all notes saved under a topic.

Example request:

```text
Show me my machine learning notes.
```

### 3. `list_study_topics`

Lists every topic that currently has saved notes.

Example request:

```text
What study-note topics have I saved?
```

### 4. `calculator`

Safely evaluates arithmetic expressions.

Example request:

```text
Calculate (120 * 0.25) + 15.
```

The calculator uses Python's Abstract Syntax Tree module instead of `eval()`. This prevents arbitrary Python code from being executed.

---

## Conversation Memory

The project uses LangGraph's `InMemorySaver`.

This allows the agent to remember earlier messages during the current program session.

Example:

```text
You: I am studying linked lists.

You: Explain insertion at the beginning.

You: Now quiz me on it.
```

The agent can understand that the quiz should be about linked-list insertion because the messages use the same conversation thread.

However, this conversation memory is temporary. It resets when the program closes.

Saved study notes are persistent because they are written to `study_notes.json`.

---

## Project Structure

The application has been refactored from one large `app.py` file into a small Python package. Each module now has one main responsibility.

```text
study-assistant-agent/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── study_notes.json
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

> `.env`, `.venv/`, and `study_notes.json` are local files and should remain excluded from Git when they contain private information.

### File descriptions

| File                                  | Responsibility                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------- |
| `app.py`                              | Small entry point that imports and runs the command-line application                        |
| `study_assistant/__init__.py`         | Marks `study_assistant` as a Python package                                                 |
| `study_assistant/agent.py`            | Creates the Groq model, conversation memory, and LangChain agent                            |
| `study_assistant/cli.py`              | Runs the terminal input loop and sends messages to the agent                                |
| `study_assistant/config.py`           | Loads `.env` and stores shared settings, paths, model configuration, and thread information |
| `study_assistant/prompts.py`          | Stores the system prompt that defines the assistant's behavior                              |
| `study_assistant/storage.py`          | Reads and writes study notes in `study_notes.json`                                          |
| `study_assistant/utils.py`            | Contains helper functions, including response formatting                                    |
| `study_assistant/tools/__init__.py`   | Imports the individual tools and groups them into `AGENT_TOOLS`                             |
| `study_assistant/tools/calculator.py` | Defines the safe calculator tool                                                            |
| `study_assistant/tools/notes.py`      | Defines the save, read, and list study-note tools                                           |
| `requirements.txt`                    | Lists the Python packages required by the project                                           |
| `.env.example`                        | Shows the required environment-variable format                                              |
| `.env`                                | Stores the private Groq API key locally; it must not be committed                           |
| `.gitignore`                          | Prevents secrets, virtual environments, caches, and local data from being committed         |
| `study_notes.json`                    | Stores saved study notes locally                                                            |
| `README.md`                           | Explains the project structure, setup, usage, and design                                    |

### Why use this structure?

Separating the code makes the project easier to:

- Read and understand
- Test one component at a time
- Add new tools without changing the entire application
- Replace the command-line interface later
- Change the model or storage system independently
- Reuse the agent from another interface, such as Streamlit or Flask

## Prerequisites

Before running the project, install:

- Python 3.10 or newer
- A code editor such as VS Code
- A free Groq API key

Create a Groq API key from the Groq Console:

```text
https://console.groq.com/keys
```

---

## Setup on macOS or Linux

### 1. Open the project folder

```bash
cd study-assistant-agent
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Create the environment file

```bash
cp .env.example .env
```

Open `.env` and replace:

```env
GROQ_API_KEY=your_groq_api_key_here
```

with your actual Groq API key.

### 5. Run the agent

Run the command from the project root, where `app.py` is located:

```bash
python app.py
```

## Setup on Windows

### 1. Open Command Prompt in the project folder

```bat
cd study-assistant-agent
```

### 2. Create and activate a virtual environment

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the dependencies

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Create the environment file

```bat
copy .env.example .env
```

Open `.env` and replace the placeholder with your actual Groq API key.

### 5. Run the agent

Run the command from the project root, where `app.py` is located:

```bat
python app.py
```

## Example Prompts

### Explanations

```text
Explain recursion in simple terms.

What is the difference between supervised and unsupervised learning?

Explain singly linked lists with an example.
```

### Quizzes and flashcards

```text
Create five flashcards about Python dictionaries.

Quiz me on gradient descent one question at a time.

Create three practice problems about arrays.
```

### Study planning

```text
Create a seven-day study plan for learning LangChain.

Help me prepare for a machine-learning interview.

Break linked lists into small topics I can study over three days.
```

### Calculator

```text
Calculate (45 * 12) / 3.

What is 18% of 250?

Calculate 2 ** 10.
```

### Saving notes

```text
Remember under Python that lists are mutable.

Save a note under machine learning: Precision measures how many predicted
positive results were actually positive.
```

### Retrieving notes

```text
Show me my Python notes.

Read my machine-learning notes.

What study topics have I saved?
```

---

## Important Parts of the Refactored Code

### Application entry point: `app.py`

`app.py` is intentionally small. Its only responsibility is to start the command-line application.

```python
from study_assistant.cli import main


if __name__ == "__main__":
    main()
```

This keeps startup logic separate from the agent implementation.

---

### Configuration: `study_assistant/config.py`

The configuration module is responsible for:

- Finding the project directory
- Loading values from `.env`
- Validating `GROQ_API_KEY`
- Storing the model name and temperature
- Defining the path to `study_notes.json`
- Defining the conversation thread configuration

Other modules import these settings instead of repeating them.

---

### System prompt: `study_assistant/prompts.py`

The assistant's role and behavioral instructions are stored separately from the Python logic.

This makes the prompt easier to read, edit, and test without changing the agent code.

---

### Study-note storage: `study_assistant/storage.py`

The storage module handles the JSON file directly. It is responsible for:

- Creating an empty notes file when necessary
- Loading saved notes
- Writing updated notes
- Keeping file-handling logic out of the LangChain tools

The tools request storage operations instead of opening the JSON file themselves.

---

### Defining tools: `study_assistant/tools/`

LangChain's `@tool` decorator converts a Python function into an action the agent can use.

The note-related tools are kept in:

```text
study_assistant/tools/notes.py
```

The calculator is kept in:

```text
study_assistant/tools/calculator.py
```

The package file below gathers all tools into one collection:

```text
study_assistant/tools/__init__.py
```

This allows `agent.py` to import one tool list instead of importing every tool separately.

---

### Creating the agent: `study_assistant/agent.py`

The agent module combines:

- The Groq-hosted language model
- The tools in `AGENT_TOOLS`
- The system prompt
- LangGraph conversation memory

Conceptually, the agent is created like this:

```python
agent = create_agent(
    model=llm,
    tools=AGENT_TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory,
)
```

The model decides whether to answer directly or call one of the available tools.

---

### Running the terminal interface: `study_assistant/cli.py`

The CLI module:

1. Displays the welcome message
2. Reads user input
3. Stops when the user enters an exit command
4. Invokes the agent
5. Uses `utils.py` to extract the final response
6. Prints the response in the terminal

Keeping the CLI separate means another interface can reuse the same agent later.

---

### Formatting responses: `study_assistant/utils.py`

Agent results can contain multiple messages, including tool calls and tool outputs.

The utility module extracts the final assistant message so the CLI only prints the answer intended for the user.

## Agent Decision Process

Suppose the user enters:

```text
Remember under algorithms that binary search requires sorted data.
```

The agent approximately follows this process:

1. Reads the user's message
2. Detects the word "remember"
3. Checks its available tools
4. Selects `save_study_note`
5. Extracts:
   - Topic: `algorithms`
   - Note: `Binary search requires sorted data`
6. Runs the Python tool
7. Receives confirmation from the tool
8. Responds to the user

For a normal explanation, the agent may decide that no tool is necessary and answer directly.

---

## Local Data Storage

Notes are stored in:

```text
study_notes.json
```

The path is defined in `study_assistant/config.py`, while reading and writing are handled by `study_assistant/storage.py`.

Initial contents:

```json
{}
```

After saving notes, the file may look like:

```json
{
  "python": ["A dictionary stores key-value pairs.", "Lists are mutable."],
  "algorithms": ["Binary search requires sorted data."]
}
```

The file is included in `.gitignore` because it may contain personal study material.

Remove `study_notes.json` from `.gitignore` only when you deliberately want to commit example notes.

## Security

### Never commit `.env`

The `.env` file contains your private API key.

The project includes this rule in `.gitignore`:

```gitignore
.env
```

Before pushing to GitHub, run:

```bash
git status
```

Make sure `.env` is not listed.

If an API key is accidentally committed:

1. Revoke it immediately in the Groq Console
2. Create a new key
3. Remove the key from Git history
4. Update your local `.env` file

### Do not hard-code API keys

Do not write this:

```python
GROQ_API_KEY = "gsk_your_real_key"
```

Always load the key from `.env`.

---

## Uploading the Project to GitHub

For the first upload:

```bash
git init
git add .
git commit -m "Add refactored LangChain study assistant"
git branch -M main
git remote add origin https://github.com/maitreyi03/study-assistant-agent.git
git push -u origin main
```

Before running `git add .`, use:

```bash
git status
```

Confirm that `.env`, `.venv/`, `__pycache__/`, and private `study_notes.json` data are not staged.

For later updates:

```bash
git add .
git commit -m "Describe the changes"
git push
```

## Common Errors

### `Missing GROQ_API_KEY`

Check that:

- The file is named exactly `.env`
- It is in the project root beside `app.py`
- It is not named `.env.txt`
- It contains a valid key

```env
GROQ_API_KEY=your_actual_key
```

Restart the program after changing the file.

---

### `ModuleNotFoundError: No module named 'study_assistant'`

Run the application from the project root rather than from inside the package directory:

```bash
cd study-assistant-agent
python app.py
```

Also check that these files exist:

```text
study_assistant/__init__.py
study_assistant/tools/__init__.py
```

---

### Another `ModuleNotFoundError`

Activate the virtual environment and reinstall the dependencies.

macOS or Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows:

```bat
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

---

### Rate-limit error

Free external LLM services impose request limits.

Possible solutions:

- Send fewer requests
- Wait for the provider's quota to reset
- Use a smaller available model
- Upgrade the provider account later if necessary

---

### Model not found

The provider may change its supported models.

Check the model setting in `study_assistant/config.py` and replace the unavailable model with another Groq model that supports tool use.

---

### Notes are not appearing

Check that:

- The application can create or access `study_notes.json`
- The file contains valid JSON
- The application has permission to write to the project folder
- `study_assistant/storage.py` is using the notes-file path from `config.py`

The default content should be:

```json
{}
```

---

### Changes in a new tool are not available

When adding another tool:

1. Define it inside `study_assistant/tools/`.
2. Import it in `study_assistant/tools/__init__.py`.
3. Add it to `AGENT_TOOLS`.
4. Restart the application.

## Current Limitations

This is a learning project, so it intentionally remains simple.

Current limitations include:

- The interface runs only in the terminal
- Conversation history disappears when the application closes
- Notes are stored in a local JSON file
- There is no user authentication
- The agent cannot currently read PDFs
- The agent does not search the internet
- Free API usage is rate-limited
- The model may occasionally select the wrong tool or misunderstand a request

---

## Possible Future Improvements

### 1. Add PDF question answering

Allow users to upload lecture notes or textbooks and ask questions about them.

Possible technologies:

- LangChain document loaders
- Text chunking
- Embedding models
- ChromaDB or FAISS
- Retrieval-augmented generation

### 2. Add a Streamlit interface

Replace the terminal with a browser-based chat application.

### 3. Add persistent conversation memory

Store chat history in SQLite so conversations remain available after restarting the program.

### 4. Add quiz tracking

Save:

- Questions attempted
- Correct and incorrect answers
- Scores by topic
- Topics that require more practice

### 5. Add note deletion and editing

Create tools such as:

```text
delete_study_note
update_study_note
clear_topic_notes
```

### 6. Add multiple student profiles

Store separate notes and history for different users.

### 7. Add a web-search tool

Allow the agent to retrieve current information from approved sources.

---

## What You Learn From This Project

By building and modifying this modular project, you learn:

- How to connect an external LLM to LangChain
- How LangChain agents differ from normal chatbots
- How to define custom tools
- How an LLM chooses and calls tools
- How to maintain temporary conversation memory
- How to store persistent data locally
- How to manage secret API keys
- How to structure a small agent-based Python project as reusable modules
- How to extend an agent with new capabilities

---

## Suggested Learning Path

1. Run the existing project
2. Test every tool
3. Read `app.py` to understand the entry point
4. Read `study_assistant/cli.py` to understand the terminal loop
5. Read `study_assistant/agent.py` to understand agent creation
6. Inspect `study_assistant/tools/` and add a new tool
7. Change the system prompt in `study_assistant/prompts.py`
8. Add note deletion or editing
9. Build a Streamlit interface that reuses the same agent
10. Add PDF retrieval and persistent chat history

## License

This project is intended for educational and personal use.

You may modify it, extend it, and use it as a portfolio project.
