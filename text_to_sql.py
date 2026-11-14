import os
from groq import Groq
from dotenv import load_dotenv
# Import the schema extractor function we built in the previous step
from schema_extractor import get_database_schema

# 1. Load environment variables and API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY is missing!")
    exit()

# 2. Initialize the Groq client
client = Groq(api_key=api_key)

def generate_sql(user_question):
    """
    This function takes a plain English question, passes it to the AI 
    along with the database schema, and returns a MySQL query.
    """
    # 3. Get the dynamic database schema
    schema = get_database_schema()
    
    # 4. Create the System Prompt (Rules for the AI)
    system_prompt = f"""
    You are an expert MySQL data analyst.
    Your job is to write a MySQL query to answer the user's question based on the provided database schema.
    
    DATABASE SCHEMA:
    {schema}
    
    RULES:
    1. Output ONLY the raw MySQL query.
    2. Do NOT include any markdown formatting (like ```sql).
    3. Do NOT include any explanations or conversational text.
    4. Make sure the query is compatible with MySQL syntax.
    """

    # 5. Call the Groq AI API
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            model="openai/gpt-oss-20b", # Our fast and active model
            temperature=0.1 # Keep it low for more deterministic and logical answers
        )
        
        # Extract and return just the SQL string
        sql_query = response.choices[0].message.content.strip()
        return sql_query
        
    except Exception as e:
        return f"❌ Failed to generate SQL. Error: {e}"

# 6. Test the function
if __name__ == "__main__":
    # Let's ask a simple business question
    test_question = "How many customers are from the North region?"
    print(f"🗣️ User Question: {test_question}")
    print("🤖 AI is generating SQL...\n")
    
    generated_sql = generate_sql(test_question)
    
    print("✅ Generated SQL Query:")
    print(generated_sql)