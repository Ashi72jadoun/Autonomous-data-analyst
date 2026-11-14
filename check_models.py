import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY is missing!")
    exit()

print("🔍 Fetching available models from Groq...\n")

try:
    # 2. Initialize the Groq client
    client = Groq(api_key=api_key)
    
    # 3. Get the list of all available models
    models = client.models.list()
    
    # 4. Print the ID (name) of each available model
    print("✅ Available Models:")
    for model in models.data:
        print(f"- {model.id}")
        
except Exception as e:
    print(f"\n❌ Failed to fetch models. Error: {e}")