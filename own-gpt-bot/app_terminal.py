"""
AskBuddy - Version 1
Run this file in the VS Code terminal.

What students learn:
1. Load an API key from .env
2. Connect Gemini with LangChain
3. Send user messages to the model
4. Keep simple conversation history
"""

# -----------------------------
# STEP 1: Load environment file
# -----------------------------
from dotenv import load_dotenv

load_dotenv()  # Reads variables from the .env file


# -----------------------------
# STEP 2: Import LangChain model
# -----------------------------
from langchain_google_genai import ChatGoogleGenerativeAI


# -----------------------------
# STEP 3: Create the Gemini model
# -----------------------------
# temperature=0.2 keeps answers more focused and consistent.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


# -----------------------------
# STEP 4: Create chat history
# -----------------------------
# We keep all previous messages in this list.
# This lets Gemini remember the current conversation.
messages = []


# -----------------------------
# STEP 5: Start the chatbot
# -----------------------------
print("\n🤖 AskBuddy is ready!")
print("Type 'exit' to stop the program.\n")

while True:

    # Ask the user for a question
    query = input("You: ").strip()

    # Stop the program when user writes exit
    if query.lower() == "exit":
        print("AskBuddy: Goodbye! 👋")
        break

    # Ignore empty input
    if not query:
        continue

    # Add the user's message to conversation history
    messages.append({
        "role": "user",
        "content": query
    })

    # Send COMPLETE conversation history to Gemini
    response = llm.invoke(messages)

    # Print Gemini's answer
    print(f"\nAskBuddy: {response.content}\n")

    # Save AI answer in conversation history
    messages.append({
        "role": "assistant",
        "content": response.content
    })
