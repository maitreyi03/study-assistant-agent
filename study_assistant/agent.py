"""Construction of the LangChain study assistant agent."""

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from study_assistant.config import (
    MODEL_NAME,
    MODEL_TEMPERATURE,
    load_environment,
)
from study_assistant.prompts import SYSTEM_PROMPT
from study_assistant.tools import AGENT_TOOLS


def create_study_agent():
    """Create and return the configured LangChain agent."""
    load_environment()

    llm = ChatGroq(
        model=MODEL_NAME,
        temperature=MODEL_TEMPERATURE,
    )

    memory = InMemorySaver()

    return create_agent(
        model=llm,
        tools=AGENT_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )
