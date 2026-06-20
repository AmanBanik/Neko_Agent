from google.adk import Workflow
from agents.nodes import sales_analyst, procurement_strategist, capital_guardrail

procurement_workflow = Workflow(name="SmartRetailProcurement")

procurement_workflow.add_node("SalesAnalyst", sales_analyst)
procurement_workflow.add_node("ProcurementStrategist", procurement_strategist)
procurement_workflow.add_node("CapitalGuardrail", capital_guardrail)

procurement_workflow.add_edge("START", "SalesAnalyst")
procurement_workflow.add_edge("SalesAnalyst", "ProcurementStrategist")
procurement_workflow.add_edge("ProcurementStrategist", "CapitalGuardrail")

def check_budget_guardrail(state):
    # Conditionally route back to the strategist if budget validation fails
    if state.get("guardrail_failed", False):
        return "ProcurementStrategist"
    return "END"

procurement_workflow.add_conditional_edges(
    "CapitalGuardrail",
    ["ProcurementStrategist", "END"],
    condition=check_budget_guardrail
)
