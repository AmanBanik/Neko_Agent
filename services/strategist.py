from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import httpx
from google.adk.agents import LlmAgent

app = FastAPI(title="Procurement Strategist Service")

@app.get("/")
def read_root():
    return {
        "status": "online", 
        "service": "Procurement Strategist Service", 
        "architecture": "Distributed A2A Network"
    }

procurement_strategist = LlmAgent(
    name="ProcurementStrategist",
    model="gemini-3.1-flash-lite",
    instruction=(
        "You are the Head Procurement Strategist. Your objective is to fulfill inventory "
        "shortfalls identified by the Analyst while optimizing for cost and lead time.\n"
        "1. Consume the Analyst's high-demand list.\n"
        "2. Call the Supplier FastMCP tool to fetch real-time wholesale pricing.\n"
        "3. Draft a precise Purchase Order (PO).\n"
        "4. If your PO is rejected by the Capital Guardrail, you MUST re-evaluate and choose "
        "a cheaper supplier or reduce quantities."
    ),
)

class RequestPayload(BaseModel):
    session_id: str
    history: list
    context: dict

@app.post("/strategize")
async def strategize(payload: RequestPayload):
    """
    Formulates a purchase order based on analysis, implementing an A2A in-loop
    retry mechanism if the downstream guardrail rejects the order.
    
    Args:
        payload (RequestPayload): The state containing the analysis report.
        
    Returns:
        dict: The final approved purchase order, or a failure state.
    """
    print(f"[Strategist] Received report from Analyst. Formulating strategy...")
    
    max_retries = 3
    for attempt in range(max_retries):
        print(f"[Strategist] Formulating Purchase Order... (Attempt {attempt + 1})")
        
        if attempt == 0:
            purchase_order = {"Widget A": 50, "Total Cost": 60000.0} 
        else:
            purchase_order = {"Widget A": 30, "Total Cost": 36000.0} 
            
        payload.context["purchase_order"] = purchase_order
        
        import os
        guardrail_url = os.environ.get("GUARDRAIL_URL", "http://localhost:8002")
        print(f"[Strategist] Forwarding PO to Capital Guardrail at {guardrail_url}...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{guardrail_url}/validate", 
                json=payload.model_dump(),
                timeout=30.0
            )
        
        result = response.json()
        if result.get("status") == "approved":
            print("[Strategist] Order approved by Guardrail. Finalizing.")
            return result
        
        print(f"[Strategist] Attempt {attempt + 1} rejected by Guardrail: {result.get('reason')}. Re-strategizing...")
        
    return {"status": "failed", "reason": "Could not meet budget constraints after 3 attempts."}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
