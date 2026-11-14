import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY is missing from the .env file!")
    exit()

print("🤖 Connecting to the AI model...")

try:
    # 2. Initialize the Groq client
    client = Groq(api_key=api_key)
    
    # 3. Send a small test message to the AI
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hi! You are my AI data analyst assistant. Reply in one short sentence."
            }
        ],
        model="openai/gpt-oss-20b", # Using an active text model from your available list
    )

    print("\n✅ AI Response Successful:")
    print(chat_completion.choices[0].message.content)
    
except Exception as e:
    print(f"\n❌ AI Connection failed. Error details: {e}")