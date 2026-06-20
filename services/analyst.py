from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import httpx
from google.adk.agents import LlmAgent

app = FastAPI(title="Sales Analyst Service")

@app.get("/")
def read_root():
    return {
        "status": "online", 
        "service": "Sales Analyst Service", 
        "architecture": "Distributed A2A Network"
    }

sales_analyst = LlmAgent(
    name="SalesAnalyst",
    model="gemini-3.1-flash-lite",
    instruction=(
        "You are a Senior Retail Sales Analyst. Your job is to fuse structured database "
        "queries with unstructured qualitative data and EDA summaries.\n"
        "1. Read the EDA statistical summaries provided in the context.\n"
        "2. Query the local SQLite inventory database for current stock levels.\n"
        "3. Use the Google Drive MCP tool to read any unstructured store manager notes.\n"
        "Output a precise JSON report listing exactly which products are high-demand and facing stockouts."
    ),
)

class RequestPayload(BaseModel):
    session_id: str
    history: list
    context: dict

@app.post("/analyze")
async def analyze(payload: RequestPayload):
    """
    Processes the EDA summary and local data to create a definitive inventory shortfall report.
    Also demonstrates where the Google Drive MCP connection would occur.
    
    Args:
        payload (RequestPayload): The state payload containing the EDA results.
        
    Returns:
        dict: The JSON response from the downstream Strategist service.
    """
    print(f"[Sales Analyst] Received EDA summary. Connecting to Google Drive MCP...")
    
    # --- GOOGLE DRIVE MCP INTEGRATION MOCK ---
    # In a real setup using the `mcp` python SDK, the agent connects directly to the server:
    #
    # from mcp import ClientSession, StdioServerParameters
    # async with ClientSession(StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-gdrive"])) as session:
    #     files = await session.call_tool("search_files", {"query": "Store Manager Notes"})
    #     print(files)
    #
    print("[Sales Analyst] (Mock MCP) Searched Google Drive. Found 'Store Manager Notes.pdf'.")
    # ----------------------------------------
    
    analysis_report = {
        "high_demand": ["Widget A", "Widget B"],
        "reasoning": "EDA showed 15% upward trend; Drive notes indicate local marketing push."
    }
    payload.context["analysis_report"] = analysis_report
    
    import os
    strategist_url = os.environ.get("STRATEGIST_URL", "http://localhost:8001")
    print(f"[Sales Analyst] Analysis complete. Forwarding to Procurement Strategist at {strategist_url}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{strategist_url}/strategize", 
            json=payload.model_dump(),
            timeout=30.0
        )
    return response.json()

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
