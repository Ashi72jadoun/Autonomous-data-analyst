from sqlalchemy import create_engine, text
import urllib.parse

# 1. Database Credentials
DB_USER = "root"

# Put your actual root password here
raw_password = "AshishThakur@18"

# 2. Safely encode the password
DB_PASSWORD = urllib.parse.quote_plus(raw_password)

DB_HOST = "localhost"
DB_NAME = "retail_bi"

# 3. Create the connection engine
connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string)

# 4. Define the diverse dummy data 
# Using INSERT IGNORE prevents crash if the data already exists
# Using IDs starting from 1001 guarantees we don't hit old test data
insert_queries = """
INSERT IGNORE INTO customers (customer_id, customer_name, region, signup_date) VALUES 
(1001, 'Rahul Verma', 'South', '2023-05-12'),
(1002, 'Priya Singh', 'East', '2023-06-18'),
(1003, 'Amit Patel', 'West', '2023-07-22'),
(1004, 'Neha Gupta', 'South', '2023-08-05'),
(1005, 'Karan Kumar', 'East', '2023-09-11');

INSERT IGNORE INTO products (product_id, product_name, category, unit_price, unit_cost) VALUES 
(1001, 'Office Chair', 'Furniture', 120.00, 80.00),
(1002, 'Wireless Mouse', 'Electronics', 25.00, 15.00),
(1003, 'Cotton T-Shirt', 'Clothing', 15.00, 8.00),
(1004, 'Desk Lamp', 'Furniture', 45.00, 25.00),
(1005, 'Bluetooth Speaker', 'Electronics', 60.00, 40.00);

INSERT IGNORE INTO orders (order_id, customer_id, product_id, order_date, quantity) VALUES 
(1001, 1001, 1001, '2023-10-01', 5),
(1002, 1002, 1002, '2023-10-05', 15),
(1003, 1003, 1003, '2023-10-10', 20),
(1004, 1004, 1004, '2023-10-15', 8),
(1005, 1005, 1005, '2023-10-20', 12),
(1006, 1001, 1003, '2023-10-22', 10),
(1007, 1002, 1001, '2023-10-25', 2),
(1008, 1003, 1005, '2023-10-28', 5);
"""

# 5. Execute the insertion safely
print("⚙️ Inserting data into the database...")

try:
    with engine.begin() as conn:
        for query in insert_queries.strip().split(';'):
            if query.strip():
                conn.execute(text(query))
    print("✅ Dummy data successfully added to the database!")
except Exception as e:
    print(f"❌ Error inserting data: {e}")