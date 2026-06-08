import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI lead qualification caller.

Your goals:
1. Determine if the customer is interested.
2. Ask their budget.
3. Ask purchase timeline.
4. Keep responses short.
5. Ask only one question at a time.

After collecting enough information,
politely end the conversation.
"""

chat = client.chats.create(
    model="gemini-2.5-flash"
)

print("\nAI Lead Qualification Demo")
print("-" * 40)

while True:
    user_input = input("\nCustomer: ")

    if user_input.lower() == "exit":
        break

    response = chat.send_message(
        f"{SYSTEM_PROMPT}\n\nCustomer: {user_input}"
    )

    print("\nAI:", response.text)