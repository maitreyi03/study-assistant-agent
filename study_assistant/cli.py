"""Command-line interface for the Personal Study Assistant."""

from study_assistant.agent import create_study_agent
from study_assistant.config import THREAD_ID
from study_assistant.utils import message_content_to_text


def main() -> None:
    """Start the interactive terminal application."""
    agent = create_study_agent()

    print("=" * 64)
    print("Personal Study Assistant")
    print("Powered by LangChain and Groq")
    print("Enter 'exit' or 'quit' to close the program.")
    print("=" * 64)

    config = {
        "configurable": {
            "thread_id": THREAD_ID,
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
