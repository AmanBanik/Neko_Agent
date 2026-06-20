# Smart Retail B2B Procurement Guardrail
## Enterprise-Grade Distributed Multi-Agent Architecture with Financial Guardrails

[![Render Deployment](https://img.shields.io/badge/Deployment-Render-purple.svg)](https://neko-agent.onrender.com)
[![Framework](https://img.shields.io/badge/Framework-Google%20ADK%202.0-blue.svg)](https://github.com/google/adk)

---

## 🎯 Project Overview
This project is a Kaggle hackathon submission for the **Business Agent Track**. It demonstrates how to transition AI agents from unreliable, monolithic chat scripts into a robust **Distributed Agent-to-Agent (A2A) Microservice Architecture**. 

By decentralizing tasks into isolated FastAPI microservices, the system automates retail inventory analysis, negotiates wholesale purchase orders using external MCP tools, and enforces strict financial budgets through an intelligent looping guardrail.

---

## 📉 The Problem
When enterprises deploy AI agents for procurement and B2B operations, they often fail because:
- **Monolithic Bottlenecks:** A single agent tries to do data science, analytics, and purchasing all at once.
- **Budget Hallucinations:** Agents place massive wholesale orders that violate corporate financial constraints.
- **Siloed Data:** Agents cannot easily merge structured database queries with unstructured Google Drive notes.

These failures lead to overspending, stockouts, and broken supply chains.

---

## ✅ Our Solution
### **Distributed A2A Choreography**
We solved these problems by splitting the workload across isolated microservices that communicate over standard HTTP REST APIs.

Key capabilities:
- **True A2A Orchestration:** Agents pass context sequentially over the network.
- **Intricate Branching Logic:** Dedicated EDA tools process messy `.xlsx` files into clean `.csv` data.
- **In-Loop Financial Correction:** If a proposed order violates the budget, the Guardrail rejects it, forcing the Strategist to retry with a cheaper configuration.
- **Cloud-Ready Persistence:** Fully integrated with a live PostgreSQL Supabase database.

---

## 🏗️ Architecture
The system relies on lightweight, containerizable FastAPI services running Google's `adk.agents.LlmAgent`.

```mermaid
graph TD
    Client[client.py / Trigger] --> EDA[EDA Data Scientist Port 7999]
    
    subgraph "The Analysis Layer"
    EDA --> Analyst[Sales Analyst Port 8000]
    Analyst -.-> GDrive[(Google Drive MCP)]
    Analyst -.-> DB[(Supabase PostgreSQL)]
    end

    subgraph "The Execution & Safety Layer"
    Strategist[Procurement Strategist Port 8001]
    Guardrail[Capital Guardrail Port 8002]
    Strategist <-->|In-Loop Retries| Guardrail
    end

    Analyst --> Strategist
    Strategist -.-> Supplier[(Supplier FastMCP Port)]
```

---

## 🔑 Key Components
### **Capital Guardrail (⭐ Star Component)**
- The financial firewall. It strictly rejects any Purchase Order exceeding ₹50,000, forcing upstream agents to correct their math.

### **Procurement Strategist**
- Calls the custom FastMCP server to fetch real-time wholesale pricing and formulates the purchase order. 

### **Sales Analyst**
- Fuses structured Postgres queries with unstructured qualitative data (via Google Drive MCP mock).

### **EDA Agent**
- Dedicated data science entry point. Converts `.xlsx` to `.csv` and uses native Python tools (Pandas/Plotly) to extract statistical trends.

---

## 🤖 AI Integration Summary
| Component | Model | Purpose | Framework |
|----------|--------|---------|-----------|
| EDA Agent | Gemini 3.1 Flash Lite | Pandas/Plotly Data Science | FastAPI + ADK |
| Analyst | Gemini 3.1 Flash Lite | Data Fusion & Postgres SQL | FastAPI + ADK |
| Strategist| Gemini 3.1 Flash Lite | MCP Tool Calling & PO Drafting | FastAPI + ADK |
| Guardrail | Gemini 3.1 Flash Lite | Strict Budget Validation | FastAPI + ADK |

---

## 🚀 Quick Start
### 1. Configure Secrets
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
Bootstrap the Supabase PostgreSQL tables:
```bash
python init_db.py
```

### 4. Run Locally (Microservice Mode)
Open 4 separate terminals and start the services:
```bash
python services/eda.py
python services/analyst.py
python services/strategist.py
python services/guardrail.py
```

Trigger the pipeline in a 5th terminal:
```bash
python client.py
```

---

## 📖 Usage Examples
### Case 1: Raw Local Data (The EDA Pipeline)
If you have local raw sales data, simply feed the filename (e.g., `Q3_Regional_Sales.xlsx`) into the `client.py` payload. The **EDA Agent** will automatically detect the `.xlsx` format, convert it to a `.csv` via custom Python tools, and run statistical trend analysis before passing the insights downstream.

### Case 2: Unstructured Cloud Data (The Drive MCP Pipeline)
If regional managers leave qualitative feedback (like "Widget A is flying off shelves!") in a shared Google Drive document, you don't need to manually feed it. The **Analyst Agent** is equipped with a Google Drive MCP tool. It dynamically searches the cloud drive, reads the unstructured notes, and fuses that context with its structured Postgres database queries.

---

## ☁️ Deployment (Render & Supabase)
This project is fully Docker/Cloud Run/Render ready. Because we use dynamic `$PORT` assignment and `os.environ` routing, you can deploy each `services/*.py` file as an independent Render Web Service.

1. Connect your GitHub Repo to Render.
2. Spin up 4 Web Services (one for each python script).
3. Copy the resulting `.onrender.com` URLs into the Environment Variables dashboard.

---

## 🛡️ Security & Compliance
### In-Loop Self Correction
If a request violates the financial policy, execution does not crash—it self-corrects.

**Example Log Output:**
```
[Strategist] Forwarding PO to Capital Guardrail...
[Strategist] Attempt 1 rejected by Guardrail: Cost ₹60000.0 exceeds ₹50,000 budget limit. Re-strategizing...
[Strategist] Formulating Purchase Order... (Attempt 2)
[Strategist] Order approved by Guardrail. Finalizing.
```
