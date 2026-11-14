import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. .env file se secure variables load karein
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 2. SQLAlchemy connection string banayein
# Format: mysql+mysqlconnector://user:password@host/database
connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

print("Database se connect ho rahe hain...")

try:
    # 3. Database Engine create karein
    engine = create_engine(connection_string)
    
    # 4. Ek safe, fixed SQL query likhein
    query = "SELECT * FROM products LIMIT 5;"
    
    # 5. Query ko sidha Pandas DataFrame mein load karein
    df = pd.read_sql(query, engine)
    
    print("\n✅ Connection Successful! Yeh rahe Products table ke data:\n")
    print(df)
    
except Exception as e:
    print(f"\n❌ Connection failed. Error details: {e}")