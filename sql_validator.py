import re

def is_safe_sql(query: str) -> tuple[bool, str]:
    """
    Validates that the SQL query is strictly read-only (SELECT / WITH) 
    and blocks any dangerous data-modification keywords.
    """
    if not query or not isinstance(query, str):
        return False, "Query is empty or invalid."

    # Convert to uppercase for safe keyword checking
    query_upper = query.strip().upper()

    # Clean markdown formatting if present
    query_cleaned = query_upper.replace("```SQL", "").replace("```", "").strip()
    
    # 1. Must start with SELECT or WITH (for CTEs/Window functions)
    if not (query_cleaned.startswith("SELECT") or query_cleaned.startswith("WITH")):
        return False, "Security Error: Only SELECT queries are allowed."

    # 2. Block dangerous keywords that can alter or delete data
    dangerous_keywords = [
        "DROP", "DELETE", "INSERT", "UPDATE", "ALTER", 
        "TRUNCATE", "REPLACE", "CREATE", "GRANT", "REVOKE"
    ]

    for keyword in dangerous_keywords:
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, query_cleaned):
            return False, f"Security Error: Forbidden keyword '{keyword}' detected."

    return True, "Query is safe."

if __name__ == "__main__":
    test_q = "SELECT * FROM customers;"
    print(is_safe_sql(test_q))