import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_database_schema():
    """
    This function connects to the MySQL database and extracts 
    the names of all tables and their columns.
    """
    # Create the connection engine
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(connection_string)
    
    # 2. Use SQLAlchemy 'inspect' to examine the database structure
    inspector = inspect(engine)
    schema_info = []
    
    # 3. Loop through each table and get its column names
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Extract just the name of each column
        column_names = [col['name'] for col in columns]
        # Format the output cleanly
        schema_info.append(f"Table: {table_name} | Columns: {', '.join(column_names)}")
        
    return "\n".join(schema_info)

# 4. Test the function if this file is run directly
if __name__ == "__main__":
    print("🔍 Extracting Database Schema...\n")
    try:
        schema = get_database_schema()
        print("✅ Database Schema Extracted Successfully:\n")
        print(schema)
    except Exception as e:
        print(f"❌ Failed to extract schema. Error: {e}")