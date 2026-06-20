from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import LlmAgent

app = FastAPI(title="Capital Guardrail Service")

capital_guardrail = LlmAgent(
    name="CapitalGuardrail",
    model="gemini-3.1-flash-lite",
    instruction=(
        "You are the strict Financial Controller (Capital Guardrail). Your sole responsibility "
        "is to ensure corporate fiscal compliance.\n"
        "1. Inspect every proposed Purchase Order.\n"
        "2. Calculate the total cost.\n"
        "3. Reject ANY order that exceeds ₹50,000 per cycle. No exceptions.\n"
        "4. If rejecting, provide a clear reason so the Strategist can correct it."
    ),
)

class RequestPayload(BaseModel):
    session_id: str
    history: list
    context: dict

@app.post("/validate")
async def validate(payload: RequestPayload):
    """
    Validates the purchase order against hardcoded financial constraints.
    
    Args:
        payload (RequestPayload): The state containing the proposed purchase order.
        
    Returns:
        dict: An approval or rejection status with a reason.
    """
    po = payload.context.get("purchase_order", {})
    cost = po.get("Total Cost", 0)
    
    print(f"[Guardrail] Validating Purchase Order... Total Cost: ₹{cost}")
    
    if cost <= 50000:
        print("[Guardrail] Validation PASSED. Budget under ₹50,000.")
        return {"status": "approved", "final_context": payload.context}
    else:
        print("[Guardrail] Validation FAILED. Budget exceeded.")
        return {"status": "rejected", "reason": f"Cost ₹{cost} exceeds ₹50,000 budget limit."}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
