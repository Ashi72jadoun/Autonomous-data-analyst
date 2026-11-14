import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Import all agent modules
from text_to_sql import generate_sql
from sql_validator import is_safe_sql
from data_visualizer import generate_chart
from insight_generator import generate_insights

# 1. Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def run_agent(question):
    """
    Complete Autonomous Data Analyst Workflow:
    Question -> SQL -> Validation -> Execution -> Data -> Chart -> Business Insights
    """
    print(f"\n🗣️ Question: {question}")
    
    # Step 1: Generate SQL using AI
    print("🤖 Thinking... (Generating SQL)")
    sql_query = generate_sql(question)
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    print(f"📄 Generated Query: {sql_query}")
    
    # Step 2: Validate SQL safety
    print("🛡️ Checking query safety...")
    is_safe, message = is_safe_sql(sql_query)
    if not is_safe:
        print(f"❌ Query Rejected: {message}")
        return None
        
    print("✅ Query is safe to execute.")
    
    # Step 3: Execute SQL on MySQL database
    print("⚙️ Executing query in MySQL...")
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    try:
        engine = create_engine(connection_string)
        df = pd.read_sql(sql_query, engine)
        
        if df.empty:
            print("⚠️ The query ran successfully, but no data was found.")
            return df
            
        print("\n📊 Final Data Table:\n")
        print(df.to_string(index=False)) 
        
        # Step 4: Automate Visualization
        print("\n🎨 Attempting to generate a chart...")
        chart_success = generate_chart(df, title=question)
        if chart_success:
            print("✨ Cyber Dark Chart saved as 'latest_chart.png'.")
            
        # Step 5: Generate Business Insights
        print("\n💡 Generating Business Insights...")
        insights = generate_insights(question, df)
        print("\n=================== EXECUTIVE INSIGHTS ===================")
        print(insights)
        print("==========================================================")
        
        return df
        
    except Exception as e:
        print(f"\n❌ Error executing query: {e}")
        return None

# Run complete pipeline test
if __name__ == "__main__":
    run_agent("Which region generated the highest number of orders?")