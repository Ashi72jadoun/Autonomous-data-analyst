import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY is missing!")
    exit()

client = Groq(api_key=api_key)

def generate_insights(user_question, df):
    """
    Takes the user's question and the returned Pandas DataFrame,
    and uses AI to generate short, grounded business insights.
    """
    if df is None or df.empty:
        return "No data available to generate insights."

    # Convert DataFrame to string format for the prompt
    data_str = df.to_string(index=False)

    system_prompt = """
    You are an expert Senior Business Intelligence Analyst.
    Your job is to analyze the provided SQL Query Result and explain the business findings concisely.

    RULES:
    1. Ground all claims strictly in the provided data. Do NOT invent numbers or outside facts.
    2. Provide exactly 2 or 3 short bullet points:
       - **Direct Answer**: Clear statement of the primary result.
       - **Key Takeaway**: Notable ranking, difference, or comparison.
       - **Business Implication**: Concise advice or observation based ONLY on this data.
    3. Keep tone executive, professional, and clear.
    """

    user_prompt = f"""
    User Question: {user_question}
    
    Data Result:
    {data_str}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-20b",
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"❌ Failed to generate insights. Error: {e}"

# Test the insight generator
if __name__ == "__main__":
    import pandas as pd
    test_data = pd.DataFrame({'Category': ['Furniture', 'Electronics', 'Appliances'], 'Quantity': [19, 10, 6]})
    test_question = "Show total quantity ordered for each product category."
    
    print("💡 Testing Insight Generator...\n")
    insights = generate_insights(test_question, test_data)
    print(insights)