from google.adk.agents import LlmAgent

sales_analyst = LlmAgent(
    name="SalesAnalyst",
    model="gemini-3.1-flash-lite",
    system_instruction="Query local store histories and identify high-demand items.",
)

procurement_strategist = LlmAgent(
    name="ProcurementStrategist",
    model="gemini-3.1-flash-lite",
    system_instruction="Consume analyst reports, call the supplier MCP tool, and match inventory shortfalls with wholesale purchase recommendations.",
)

capital_guardrail = LlmAgent(
    name="CapitalGuardrail",
    model="gemini-3.1-flash-lite",
    system_instruction="Validate proposed orders against a fixed financial budget (e.g., maximum ₹50,000 per order cycle).",
)
