import sqlite3
import os

DB_PATH = "src/data/nodes.db"

def verify_db():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database file not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
        
        if tables:
            first_table = tables[0][0]
            print(f"--- Schema for {first_table} ---")
            cursor.execute(f"PRAGMA table_info({first_table})")
            columns = cursor.fetchall()
            for col in columns:
                print(col)
                
        conn.close()
        print("Database verification successful.")
    except Exception as e:
        print(f"ERROR: Failed to connect or query database: {e}")

if __name__ == "__main__":
    verify_db()
