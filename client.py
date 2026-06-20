import httpx
import json

def run_procurement():
    """
    Entrypoint script that kicks off the entire Distributed A2A Procurement Pipeline.
    It initiates the process by sending the starting context to the EDA service.
    
    Args:
        None
        
    Returns:
        None
    """
    print("Initiating Distributed A2A Procurement Pipeline...")
    
    initial_payload = {
        "session_id": "demo-session-123",
        "history": [],
        "context": {
            "gdrive_file_name": "Q3_Regional_Sales.xlsx"
        }
    }
    
    import os
    eda_url = os.environ.get("EDA_URL", "http://localhost:7999")
    
    # Send request to the very first microservice (EDA Agent)
    with httpx.Client() as client:
        try:
            print(f"Client -> Sending raw data references to EDA Agent at {eda_url}...")
            response = client.post(f"{eda_url}/eda", json=initial_payload, timeout=30.0)
            result = response.json()
            
            print("\n==================================")
            print("      FINAL PIPELINE RESULT       ")
            print("==================================")
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"Pipeline failed: {e}")
            print("Make sure all 4 services are running on ports 7999, 8000, 8001, and 8002.")

if __name__ == "__main__":
    run_procurement()
