import os
import pandas as pd
from typing import TypedDict, Optional
from sqlalchemy import create_engine
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

# Import our existing backend modules
from text_to_sql import generate_sql
from sql_validator import is_safe_sql
from data_visualizer import generate_chart
from insight_generator import generate_insights

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 1. Define the Agent State
class AgentState(TypedDict):
    question: str
    sql_query: Optional[str]
    is_safe: bool
    data: Optional[pd.DataFrame]
    insights: Optional[str]
    error: Optional[str]
    retry_count: int

# 2. Define the Nodes (The Work Stations)
def generate_sql_node(state: AgentState):
    print(f"📍 NODE: Generating SQL (Attempt {state['retry_count'] + 1})...")
    
    # If there's an error from a previous attempt, feed it back to the AI
    prompt = state["question"]
    if state["error"] and state["retry_count"] > 0:
        prompt += f"\n\nWARNING: Your previous SQL query failed with this error: {state['error']}. Please fix the syntax or column names and provide a corrected query."
        
    sql_query = generate_sql(prompt)
    clean_sql = sql_query.replace("```sql", "").replace("```", "").strip()
    
    print(f"📄 Generated Query: {clean_sql}")
    return {"sql_query": clean_sql}

def validate_sql_node(state: AgentState):
    print("📍 NODE: Validating SQL Safety...")
    is_safe, message = is_safe_sql(state["sql_query"])
    
    if not is_safe:
        print(f"❌ Security Alert: {message}")
        return {"is_safe": False, "error": message}
        
    print("✅ SQL is safe.")
    return {"is_safe": True, "error": None}

def execute_sql_node(state: AgentState):
    print("📍 NODE: Executing SQL...")
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(connection_string)
    
    try:
        df = pd.read_sql(state["sql_query"], engine)
        print("✅ Data retrieved successfully!")
        
        # Automatically generate chart if possible
        generate_chart(df, title=state["question"])
        
        return {"data": df, "error": None}
    except Exception as e:
        error_msg = str(e)
        print(f"⚠️ SQL Execution Failed: {error_msg}")
        return {"error": error_msg, "retry_count": state["retry_count"] + 1}

def generate_insights_node(state: AgentState):
    print("📍 NODE: Generating Insights...")
    insights = generate_insights(state["question"], state["data"])
    return {"insights": insights}

# 3. Define the Routers (The Brain)
def route_after_validation(state: AgentState):
    if state["is_safe"]:
        return "execute_sql"
    return END

def route_after_execution(state: AgentState):
    # If there is no error, proceed to insights
    if not state.get("error"):
        return "generate_insights"
    
    # If there is an error, check if we have retries left
    if state["retry_count"] < 3:
        print("🔄 Self-Healing Triggered: Routing back to SQL Generation...")
        return "generate_sql"
    
    print("❌ Max retries reached. Aborting.")
    return END

# 4. Build and Compile the Graph
workflow = StateGraph(AgentState)

workflow.add_node("generate_sql", generate_sql_node)
workflow.add_node("validate_sql", validate_sql_node)
workflow.add_node("execute_sql", execute_sql_node)
workflow.add_node("generate_insights", generate_insights_node)

workflow.set_entry_point("generate_sql")

# Add standard edges
workflow.add_edge("generate_sql", "validate_sql")
workflow.add_edge("generate_insights", END)

# Add conditional routing edges
workflow.add_conditional_edges("validate_sql", route_after_validation)
workflow.add_conditional_edges("execute_sql", route_after_execution)

app_graph = workflow.compile()

# Test the fully functional graph
if __name__ == "__main__":
    print("🚀 Initializing Autonomous LangGraph Test...\n")
    initial_state = {
        "question": "Show total quantity ordered for each product category.",
        "sql_query": None,
        "is_safe": True,
        "data": None,
        "insights": None,
        "error": None,
        "retry_count": 0
    }
    
    final_state = app_graph.invoke(initial_state)
    print("\n=================== FINAL INSIGHTS ===================")
    print(final_state.get("insights", "No insights generated."))