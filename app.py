import os
import requests
from dotenv import load_dotenv

# -----------------------------------
# Load API key from .env
# -----------------------------------
load_dotenv()

API_KEY = os.getenv("DIFY_API_KEY")

if not API_KEY:
    print("❌ DIFY_API_KEY not found!")
    print("Check your .env file.")
    exit()

print("✅ API Key loaded successfully")


# -----------------------------------
# Dify API
# -----------------------------------
URL = "https://api.dify.ai/v1/chat-messages"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# -----------------------------------
# Chat function
# -----------------------------------
def ask_dify(question, conversation_id=""):

    data = {
        "inputs": {},
        "query": question,
        "response_mode": "blocking",
        "user": "student"
    }

    # Continue previous conversation if available
    if conversation_id:
        data["conversation_id"] = conversation_id

    try:

        response = requests.post(
            URL,
            headers=HEADERS,
            json=data,
            timeout=120
        )

        # Convert response to JSON
        result = response.json()

        # Success
        if response.status_code == 200:

            answer = result.get("answer", "")
            new_conversation_id = result.get(
                "conversation_id",
                conversation_id
            )

            return answer, new_conversation_id

        # Unauthorized
        elif response.status_code == 401:

            print("❌ Error 401: Invalid Dify API key.")
            print("Generate a new API key in Dify.")

        # Bad request
        elif response.status_code == 400:

            print("❌ Error 400:", result)

        # Other errors
        else:

            print("❌ Error:", result)

    except requests.exceptions.Timeout:

        print("❌ Request timed out.")

    except requests.exceptions.ConnectionError:

        print("❌ Internet connection error.")

    except Exception as e:

        print("❌ Error:", e)

    return None, conversation_id


# -----------------------------------
# Main chatbot
# -----------------------------------
print("\n" + "=" * 50)
print("🤖 LANGCHAIN LEARNING ASSISTANT")
print("=" * 50)

print("Ask questions about LangChain, Python, AI and GenAI.")
print("Type 'exit' to stop.\n")


conversation_id = ""


while True:

    question = input("You: ").strip()

    # Empty question
    if not question:
        print("⚠️ Please enter a question.")
        continue

    # Exit
    if question.lower() == "exit":
        print("\nGoodbye! 👋")
        break

    # Ask Dify
    answer, conversation_id = ask_dify(
        question,
        conversation_id
    )

    # Display answer
    if answer:
        print("\nAssistant:", answer)
        print()