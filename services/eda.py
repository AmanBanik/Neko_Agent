from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import httpx
import os
from google.adk.agents import LlmAgent

app = FastAPI(title="EDA Agent Service")

@app.get("/")
def read_root():
    return {
        "status": "online", 
        "service": "EDA Agent Service", 
        "architecture": "Distributed A2A Network"
    }

def convert_xlsx_to_csv(filepath: str) -> str:
    """
    Converts an Excel file (.xlsx) into a CSV format.
    
    Args:
        filepath (str): The absolute or relative path to the .xlsx file.
        
    Returns:
        str: The path to the newly created .csv file.
    """
    # Mock implementation
    print(f"[EDA Tool] Converting {filepath} to CSV...")
    csv_path = filepath.replace(".xlsx", ".csv")
    return csv_path

def generate_sales_plot(csv_path: str, x_col: str, y_col: str) -> str:
    """
    Generates a statistical plot using Plotly/Seaborn to visualize trends.
    
    Args:
        csv_path (str): Path to the CSV data file.
        x_col (str): The column name to use for the X-axis (e.g., 'Date').
        y_col (str): The column name to use for the Y-axis (e.g., 'Sales').
        
    Returns:
        str: A summary of the visual trend or path to the saved HTML chart.
    """
    # Mock implementation
    print(f"[EDA Tool] Generating plot for {x_col} vs {y_col} from {csv_path}...")
    return f"Plot generated showing a 15% upward trend in {y_col}."

eda_agent = LlmAgent(
    name="EdaAgent",
    model="gemini-3.1-flash-lite",
    instruction=(
        "You are an expert Data Scientist specializing in Exploratory Data Analysis (EDA) "
        "for retail operations. You use pandas, seaborn, and plotly to extract insights.\n"
        "Your task is to review raw file references, convert them to CSV if they are XLSX, "
        "and generate statistical summaries (mean, variance, seasonality) and visualizations.\n"
        "Always rely on the provided tools to process files."
    ),
    tools=[convert_xlsx_to_csv, generate_sales_plot]
)

class RequestPayload(BaseModel):
    session_id: str
    history: list
    context: dict

@app.post("/eda")
async def run_eda(payload: RequestPayload):
    """
    Entrypoint for the EDA Microservice.
    
    Args:
        payload (RequestPayload): The state containing session and context information.
        
    Returns:
        dict: The JSON response from the downstream Analyst service, or failure state.
    """
    print(f"[EDA Agent] Received raw data references for session: {payload.session_id}")
    
    gdrive_url = payload.context.get("gdrive_url")
    file_reference = payload.context.get("file_reference")
    
    if gdrive_url:
        print(f"[EDA Agent] Connecting to Google Drive MCP...")
        print(f"[EDA Agent] Authenticating and downloading dataset from: {gdrive_url}")
        raw_file = "downloaded_cloud_sales.xlsx"
    elif file_reference:
        raw_file = file_reference
    else:
        raw_file = "sales_q3.xlsx"
    
    if raw_file.endswith(".xlsx"):
        csv_file = convert_xlsx_to_csv(raw_file)
    else:
        csv_file = raw_file
        
    trend_summary = generate_sales_plot(csv_file, "Date", "Daily_Revenue")
    
    payload.context["eda_summary"] = f"Data cleaned. {trend_summary}"
    
    analyst_url = os.environ.get("ANALYST_URL", "http://localhost:8000")
    print(f"[EDA Agent] EDA complete. Forwarding clean statistics to Sales Analyst at {analyst_url}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{analyst_url}/analyze", 
            json=payload.model_dump(),
            timeout=30.0
        )
    return response.json()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7999))
    uvicorn.run(app, host="0.0.0.0", port=port)
