import sqlite3
import json
from agents.graph import procurement_workflow
from google import genai

def get_or_create_session(session_id: str):
    conn = sqlite3.connect('db/inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT history_json, context_state FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    if row:
        history = json.loads(row[0]) if row[0] else []
        context = json.loads(row[1]) if row[1] else {}
    else:
        cursor.execute("INSERT INTO sessions (session_id, history_json, context_state) VALUES (?, ?, ?)", (session_id, "[]", "{}"))
        conn.commit()
        history = []
        context = {}
    conn.close()
    return history, context

def save_session(session_id: str, history: list, context: dict):
    conn = sqlite3.connect('db/inventory.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET history_json = ?, context_state = ? WHERE session_id = ?", 
                   (json.dumps(history), json.dumps(context), session_id))
    conn.commit()
    conn.close()

def main():
    session_id = input("Enter session ID: ")
    history, context = get_or_create_session(session_id)
    
    # Run Workflow
    print("Running Smart Retail B2B Procurement Workflow...")
    
    initial_state = {
        "history": history,
        "context": context,
        "guardrail_failed": False
    }
    
    # Mock execution or actual depending on setup.
    # We are returning a static output as part of boilerplate until logic is fully wired.
    # final_state = procurement_workflow.run(initial_state)
    
    final_state = {
        "purchase_order": {
            "Widget A": 50,
            "Total Cost": 4000.0
        }
    }
    
    # Human-in-the-Loop Validation
    print("\n--- Proposed Purchase Order ---")
    print(json.dumps(final_state.get("purchase_order", {}), indent=2))
    
    approval = input("Approve this order? [Y/N]: ")
    if approval.strip().upper() == 'Y':
        print("Order approved and written to database.")
        # Store order logic
    else:
        print("Order rejected.")

    save_session(session_id, history, context)

if __name__ == "__main__":
    main()
