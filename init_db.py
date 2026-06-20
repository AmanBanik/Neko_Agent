import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL environment variable is not set.")
        print("Please set it in your .env file or environment variables.")
        return

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            current_stock INTEGER NOT NULL,
            reorder_level INTEGER NOT NULL,
            price REAL NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_history (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            quantity_sold INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Seed data (using ON CONFLICT DO NOTHING for PostgreSQL)
        cursor.execute('''
            INSERT INTO products (name, current_stock, reorder_level, price) 
            VALUES ('Widget A', 10, 50, 100.0) 
            ON CONFLICT (name) DO NOTHING
        ''')
        cursor.execute('''
            INSERT INTO products (name, current_stock, reorder_level, price) 
            VALUES ('Widget B', 20, 30, 200.0) 
            ON CONFLICT (name) DO NOTHING
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL Database initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")

if __name__ == '__main__':
    init_db()
