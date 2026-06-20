from fastmcp import FastMCP
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("SupplierMCP")
DB_URL = os.environ.get("DATABASE_URL")

@mcp.tool()
def fetch_supplier_catalog() -> dict:
    """Simulates an external vendor endpoint returning bulk wholesale pricing and shipping lead times."""
    return {
        "catalog": [
            {"product_name": "Widget A", "wholesale_price": 80.0, "lead_time_days": 3},
            {"product_name": "Widget B", "wholesale_price": 160.0, "lead_time_days": 5},
            {"product_name": "Widget C", "wholesale_price": 40.0, "lead_time_days": 2},
        ]
    }

@mcp.tool()
def query_local_inventory(product_name: str) -> dict:
    """Queries the PostgreSQL database for inventory levels.
    Includes strict security guardrail against SQL injection.
    """
    if not isinstance(product_name, str) or ';' in product_name or '--' in product_name:
        return {"error": "Invalid input detected."}
        
    if not DB_URL:
        return {"error": "DATABASE_URL not configured on server."}
    
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        
        # Safe parameterized query for psycopg2 (%s instead of ?)
        cursor.execute("SELECT name, current_stock, reorder_level, price FROM products WHERE name = %s", (product_name,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return {
                "name": row[0],
                "current_stock": row[1],
                "reorder_level": row[2],
                "price": row[3]
            }
        return {"error": "Product not found."}
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
