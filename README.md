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
User enters a message
        |
        v
LangChain agent receives the message
        |
        v
Groq-hosted LLM decides what to do
        |
        +-----------------------------+
        |                             |
        v                             v
Answer directly                  Call a tool
                                      |
                    +-----------------+------------------+
                    |                 |                  |
                    v                 v                  v
               Calculator       Save a note        Read notes
                    |                 |                  |
                    +-----------------+------------------+
                                      |
                                      v
                            Tool result returns
                                      |
                                      v
                       Agent creates final response
```

---

## Agent Tools

The project gives the LLM access to four tools.

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

```text
personal-study-assistant-agent/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── study_notes.json
├── setup_mac_linux.sh
├── setup_windows.bat
└── README.md
```

### File descriptions

| File                 | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| `app.py`             | Contains the agent, tools, model configuration, and command-line interface |
| `requirements.txt`   | Lists the Python libraries required by the project                         |
| `.env.example`       | Shows the required environment-variable format                             |
| `.env`               | Stores your private Groq API key locally                                   |
| `.gitignore`         | Prevents secrets and generated files from being committed                  |
| `study_notes.json`   | Stores saved notes locally                                                 |
| `setup_mac_linux.sh` | Automates setup on macOS and Linux                                         |
| `setup_windows.bat`  | Automates setup on Windows                                                 |
| `README.md`          | Explains the project and how to run it                                     |

---

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
cd personal-study-assistant-agent
```

### 2. Run the setup script

```bash
chmod +x setup_mac_linux.sh
./setup_mac_linux.sh
```

The script will:

1. Create a virtual environment
2. Activate the environment
3. Install the required packages
4. Create `.env` from `.env.example`

### 3. Add the Groq API key

Open `.env` and replace:

```env
GROQ_API_KEY=your_groq_api_key_here
```

with your actual API key.

### 4. Run the agent

```bash
source .venv/bin/activate
python app.py
```

---

## Manual Setup on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Add your API key to `.env`, then run:

```bash
python app.py
```

---

## Setup on Windows

### 1. Open Command Prompt in the project folder

```bat
cd personal-study-assistant-agent
```

### 2. Run the setup file

```bat
setup_windows.bat
```

### 3. Add the Groq API key

Open `.env` and replace the placeholder with your actual key.

### 4. Run the agent

```bat
.venv\Scripts\activate
python app.py
```

---

## Manual Setup on Windows

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

Add your API key to `.env`, then run:

```bat
python app.py
```

---

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

## Important Parts of `app.py`

### Loading the environment variable

```python
load_dotenv(PROJECT_DIR / ".env")
```

This reads values from the local `.env` file.

The application then checks that the API key exists:

```python
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("Missing GROQ_API_KEY")
```

---

### Creating the Groq model

```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
```

The model acts as the agent's reasoning engine.

A lower temperature makes the responses more consistent and less random.

---

### Defining a tool

LangChain's `@tool` decorator converts a Python function into something the agent can use.

```python
@tool
def read_study_notes(topic: str) -> str:
    """Retrieve saved study notes for a topic."""
```

The function name, parameter types, and docstring help the LLM understand when and how to call the tool.

---

### Creating the agent

```python
agent = create_agent(
    model=llm,
    tools=[
        save_study_note,
        read_study_notes,
        list_study_topics,
        calculator,
    ],
    system_prompt="...",
    checkpointer=memory,
)
```

The agent receives:

- The LLM
- The available tools
- Instructions describing its role
- A memory system

---

### Running the agent

```python
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
```

The result contains the messages generated during the agent loop, including tool calls and the final answer.

The application prints the last message:

```python
final_message = result["messages"][-1]
```

---

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

Remove `study_notes.json` from `.gitignore` if you deliberately want to commit example notes.

---

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

```bash
git init
git add .
git commit -m "Build LangChain personal study assistant"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Before running `git add .`, verify that `.env` is ignored.

---

## Common Errors

### `Missing GROQ_API_KEY`

Check that:

- The file is named exactly `.env`
- It is in the same directory as `app.py`
- It is not named `.env.txt`
- It contains a valid key

```env
GROQ_API_KEY=your_actual_key
```

Restart the program after changing the file.

---

### `ModuleNotFoundError`

Activate the virtual environment and install the dependencies again.

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

Open `app.py` and replace:

```python
model="llama-3.3-70b-versatile"
```

with another Groq model that supports tool use.

---

### Notes are not appearing

Check that:

- `study_notes.json` exists
- It contains valid JSON
- The application has permission to write to the project folder

The default content should be:

```json
{}
```

---

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

By building and modifying this project, you learn:

- How to connect an external LLM to LangChain
- How LangChain agents differ from normal chatbots
- How to define custom tools
- How an LLM chooses and calls tools
- How to maintain temporary conversation memory
- How to store persistent data locally
- How to manage secret API keys
- How to structure a small agent-based Python project
- How to extend an agent with new capabilities

---

## Suggested Learning Path

1. Run the existing project
2. Test every tool
3. Read through `app.py`
4. Change the system prompt
5. Add a new tool
6. Add note deletion
7. Build a Streamlit interface
8. Add PDF retrieval
9. Add persistent chat history
10. Deploy the application

---

## License

This project is intended for educational and personal use.

You may modify it, extend it, and use it as a portfolio project.
