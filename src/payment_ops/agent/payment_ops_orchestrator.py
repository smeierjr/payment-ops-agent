"""
Payment Operations Orchestrator - Individual payment processing with clear handoffs
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from agents.mcp.server import MCPServerStdio, MCPServerStdioParams
from agents.agent import Agent
from agents.handoffs import handoff
from agents import Runner
from agents import trace
from datetime import datetime, timezone


# Individual payment processing data models
class PaymentDecision(BaseModel):
    """LLM decision for individual payment processing"""
    payment_id: str = Field(description="Payment being processed")
    action: str = Field(
        description="PROCESS_DIRECTLY | HANDOFF_COMPLIANCE | HANDOFF_CUSTOMER_SERVICE"
    )
    reason: str = Field(description="Why this action was chosen")
    priority: str = Field(description="LOW | MEDIUM | HIGH | CRITICAL")
    context: Dict[str, Any] = Field(default_factory=dict, description="Payment details")


class PendingPaymentsList(BaseModel):
    """Structured output for pending payments retrieval"""
    payment_ids: list[str] = Field(
        description="List of pending payment IDs (e.g., ['PAY-12345', 'PAY-12346'])"
    )
    total_count: int = Field(description="Total number of pending payments found")


# Individual payment processing instructions
INDIVIDUAL_PAYMENT_INSTRUCTIONS = """You are processing a SINGLE payment for educational \
clarity in OpenAI Agent SDK patterns.

Your task is simple:
1. Get details for this ONE payment using get_payment_details
2. Analyze the payment situation
3. Make a clear decision: PROCESS_DIRECTLY | HANDOFF_COMPLIANCE | HANDOFF_CUSTOMER_SERVICE
4. Execute that decision

DECISION CRITERIA:

HANDOFF_COMPLIANCE when:
- Payment amount >= $3000 (regulatory threshold)
- Error code: COMPLIANCE_HOLD or UNKNOWN_ERROR
- Customer tier: VIP/Business with amount >= $2000

HANDOFF_CUSTOMER_SERVICE when:
- Customer tier: VIP/Business (any payment failure)
- Error code: INSUFFICIENT_FUNDS (needs customer contact)
- Error code: CARD_DECLINED (customer action required)

PROCESS_DIRECTLY when:
- Technical failures that can be retried
- Low-value standard customer payments
- Simple system errors

Execute your decision immediately:
- PROCESS_DIRECTLY: Use retry_payment or escalate_payment tools
- HANDOFF_COMPLIANCE: Call transfer_to_compliance
- HANDOFF_CUSTOMER_SERVICE: Call transfer_to_customer_service

Be decisive and clear about your reasoning for learning purposes.
"""


class PaymentOpsOrchestrator:
    """
    Simplified Payment Operations Orchestrator for individual payment processing

    Processes payments one at a time with clear, traceable handoff decisions.
    Educational focus: Understanding OpenAI Agent SDK handoff patterns.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Payment Operations Orchestrator with SDK tracing capabilities

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Cost-optimized model

        self.mcp_server: Optional[MCPServerStdio] = None
        self.compliance_agent: Optional[Agent] = None
        self.customer_service_agent: Optional[Agent] = None
        self.primary_agent: Optional[Agent] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize all agents and MCP server"""
        if self._initialized:
            return

        print("🔗 [ORCHESTRATOR] Initializing MCP server and agents...")
        await self.setup_mcp_server()
        await self.create_specialist_agents()
        await self.create_primary_agent()
        self._initialized = True
        print("✅ [ORCHESTRATOR] Initialization complete")

    async def setup_mcp_server(self):
        """Setup unified MCP server connection"""
        try:
            # Get the path to the unified MCP server script
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            mcp_server_path = os.path.join(
                project_root, "src", "payment_ops", "unified_mcp", "server.py"
            )

            # Create MCP server with stdio transport
            params = MCPServerStdioParams(
                command="uv", args=["run", "python", mcp_server_path]
            )
            self.mcp_server = MCPServerStdio(params=params)
            await self.mcp_server.connect()
            print("🔗 [ORCHESTRATOR] MCP server connected with 7 payment tools")

        except Exception as e:
            print(f"⚠️  [ORCHESTRATOR] Warning: Failed to setup MCP server: {e}")
            self.mcp_server = None

    async def create_specialist_agents(self):
        """Create specialist agents for individual payment handoffs"""
        if not self.mcp_server:
            msg = "⚠️  [ORCHESTRATOR] Warning: MCP server not available for specialist agents"
            print(msg)
            return

        print("🔨 [ORCHESTRATOR] Creating specialist agents...")

        # Create compliance specialist agent with shared MCP server
        print("🔨 [ORCHESTRATOR] Creating ComplianceSpecialist...")
        from ..agent.compliance_specialist import ComplianceSpecialist
        compliance_specialist = ComplianceSpecialist(mcp_server=self.mcp_server)
        await compliance_specialist.initialize()
        self.compliance_agent = compliance_specialist.agent

        # Create customer service specialist agent with shared MCP server
        print("🔨 [ORCHESTRATOR] Creating CustomerServiceSpecialist...")
        from ..agent.customer_service_specialist import CustomerServiceSpecialist
        customer_service_specialist = CustomerServiceSpecialist(mcp_server=self.mcp_server)
        await customer_service_specialist.initialize()
        self.customer_service_agent = customer_service_specialist.agent

    async def create_primary_agent(self):
        """Create primary orchestrator agent with handoffs"""
        print("🔨 [ORCHESTRATOR] Creating primary agent...")
        print(f"🔍 [ORCHESTRATOR] MCP server available: {self.mcp_server is not None}")
        compliance_available = self.compliance_agent is not None
        print(f"🔍 [ORCHESTRATOR] Compliance agent available: {compliance_available}")
        cs_available = self.customer_service_agent is not None
        print(f"🔍 [ORCHESTRATOR] Customer service agent available: {cs_available}")

        if (
            not self.mcp_server
            or not self.compliance_agent
            or not self.customer_service_agent
        ):
            msg = (
                "⚠️  [ORCHESTRATOR] Warning: Cannot create primary agent - "
                "dependencies not available"
            )
            print(msg)
            return

        handoffs_enabled = bool(self.compliance_agent and self.customer_service_agent)
        print(f"🔗 [ORCHESTRATOR] Handoffs enabled: {handoffs_enabled}")
        handoff_count = 2 if handoffs_enabled else 0
        print(f"🔗 [ORCHESTRATOR] Will register {handoff_count} handoff tools")

        # Import input guardrails
        from ..guardrails.input_validators import (
            validate_payment_request,
            validate_query_safety,
            validate_business_rules,
        )

        # Primary orchestrator agent for individual payment processing with input guardrails
        self.primary_agent = Agent(
            name="PaymentOpsOrchestrator",
            instructions=INDIVIDUAL_PAYMENT_INSTRUCTIONS,
            model=self.model,
            mcp_servers=[self.mcp_server],
            handoffs=(
                [
                    handoff(
                        self.compliance_agent,
                        tool_name_override="transfer_to_compliance",
                    ),
                    handoff(
                        self.customer_service_agent,
                        tool_name_override="transfer_to_customer_service",
                    ),
                ]
                if self.compliance_agent and self.customer_service_agent
                else []
            ),
            input_guardrails=[
                validate_payment_request,
                validate_query_safety,
                validate_business_rules,
            ],
        )

        # Debug: Check if handoff tools were registered
        if hasattr(self.primary_agent, 'handoffs') and self.primary_agent.handoffs:
            handoffs_count = len(self.primary_agent.handoffs)
            msg = f"✅ [ORCHESTRATOR] Primary agent has {handoffs_count} handoff(s) registered"
            print(msg)
            for i, handoff_def in enumerate(self.primary_agent.handoffs):
                try:
                    # Try different ways to get the agent name
                    print(f"  📤 Handoff {i+1}: registered successfully")
                except Exception:
                    print(f"  📤 Handoff {i+1}: registered (details unavailable)")
        else:
            print("❌ [ORCHESTRATOR] Primary agent has NO handoffs registered")

    async def process_individual_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Process a single payment with clear tracing and handoff patterns

        Args:
            payment_id: ID of payment to process

        Returns:
            Dict containing processing results and clear handoff trace
        """
        if not self._initialized:
            await self.initialize()

        if not self.primary_agent:
            return {
                "status": "error",
                "error": "Failed to initialize orchestrator",
                "payment_id": payment_id,
            }

        # Create focused workflow trace with payment ID in the name
        workflow_name = f"Payment {payment_id} Workflow"

        with trace(
            workflow_name=workflow_name,
            metadata={
                "payment_id": payment_id,
                "model": self.model,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "processing_mode": "individual_payment",
            },
        ) as workflow_trace:
            try:
                print(f"🔄 [PAYMENT {payment_id}] Starting individual processing...")

                # Prepare payment-specific message
                message = (
                    f"Process payment {payment_id}. Get details, analyze, "
                    "and make a clear decision."
                )

                # Use the Runner to execute with SDK tracing
                runner = Runner()
                response = await runner.run(
                    starting_agent=self.primary_agent, input=message
                )

                # Extract handoff information
                handoff_info = self._extract_handoff_info(response)

                result = {
                    "status": "completed",
                    "payment_id": payment_id,
                    "final_response": response.final_output,
                    "handoffs_triggered": len(handoff_info.get("handoffs", [])),
                    "agents_involved": handoff_info.get(
                        "agents_involved", ["PaymentOpsOrchestrator"]
                    ),
                    "sdk_trace_id": workflow_trace.trace_id,
                    "workflow_name": workflow_name,
                }

                handoffs_count = len(handoff_info.get('handoffs', []))
                msg = f"✅ [PAYMENT {payment_id}] Processing complete - {handoffs_count} handoffs"
                print(msg)
                return result

            except Exception as e:
                error_msg = f"Error processing payment {payment_id}: {str(e)}"
                print(f"❌ [PAYMENT {payment_id}] Error: {error_msg}")

                return {
                    "status": "error",
                    "payment_id": payment_id,
                    "error": error_msg,
                    "sdk_trace_id": workflow_trace.trace_id,
                }

    async def run(self, message: str) -> Dict[str, Any]:
        """
        Main entry point - processes payments individually for educational clarity

        Args:
            message: User message/task

        Returns:
            Dict containing results from individual payment processing
        """
        if not self._initialized:
            await self.initialize()

        # Get all pending payments first
        print("📋 [ORCHESTRATOR] Getting all pending payments...")

        # Use PaymentRetriever agent with clear JSON format instructions
        temp_agent = Agent(
            name="PaymentRetriever",
            instructions="""Use get_pending_payments to retrieve all payments, \
then return ONLY a JSON object in this exact format:

{
  "payment_ids": ["PAY-12345", "PAY-12346", "PAY-12347"],
  "total_count": 3
}

Do not include any other text, explanations, or formatting. \
Only return the JSON object.""",
            model=self.model,
            mcp_servers=[self.mcp_server] if self.mcp_server else [],
        )

        runner = Runner()
        response = await runner.run(
            starting_agent=temp_agent,
            input="Get all pending payments and return the JSON format exactly as instructed"
        )

        # Extract payment IDs from structured response
        payment_ids = self._extract_payment_ids_from_structured_response(response)

        msg = f"💳 [ORCHESTRATOR] Processing {len(payment_ids)} payments individually..."
        print(msg)

        # Process each payment individually
        all_results = []
        all_agents_involved = set(["PaymentOpsOrchestrator"])
        summary = {
            "total_payments": len(payment_ids),
            "total_handoffs": 0,
            "compliance_handoffs": 0,
            "customer_service_handoffs": 0,
            "direct_processing": 0,
        }

        for payment_id in payment_ids:
            result = await self.process_individual_payment(payment_id)
            all_results.append(result)

            # Track all agents involved across all payments
            for agent in result.get("agents_involved", []):
                all_agents_involved.add(agent)

            # Update summary
            if result["status"] == "completed":
                handoff_count = result["handoffs_triggered"]
                summary["total_handoffs"] += handoff_count

                if handoff_count == 0:
                    summary["direct_processing"] += 1
                else:
                    # Count handoff types based on agents involved
                    agents = result["agents_involved"]
                    if "ComplianceSpecialist" in agents:
                        summary["compliance_handoffs"] += 1
                    if "CustomerServiceSpecialist" in agents:
                        summary["customer_service_handoffs"] += 1

        return {
            "status": "completed",
            "processing_mode": "individual_payments",
            "total_turns": 1,
            "orchestration_summary": {
                "primary_agent": "PaymentOpsOrchestrator",
                "handoffs_triggered": summary["total_handoffs"],
                "agents_involved": list(all_agents_involved),
                "decision_points": [
                    f"Processed {len(payment_ids)} payments individually"
                ],
            },
            "summary": summary,
            "individual_results": all_results,
            "final_response": (
                f"Processed {len(payment_ids)} payments individually. "
                f"Total handoffs: {summary['total_handoffs']}"
            ),
        }

    def _extract_handoff_info(self, response) -> Dict[str, Any]:
        """Extract handoff information from SDK response - using last_agent as definitive source"""
        handoff_info = {
            "handoffs": [],
            "agents_involved": ["PaymentOpsOrchestrator"],
            "decision_points": [],
        }

        # Use last_agent field as the definitive source of truth for handoffs
        if hasattr(response, "last_agent") and response.last_agent:
            last_agent_name = str(response.last_agent)

            # Check the agent name more precisely - look for the actual name
            if hasattr(response.last_agent, "name"):
                agent_name = response.last_agent.name
            else:
                # Fallback to string parsing if name attribute not available
                if "name='ComplianceSpecialist'" in last_agent_name:
                    agent_name = "ComplianceSpecialist"
                elif "name='CustomerServiceSpecialist'" in last_agent_name:
                    agent_name = "CustomerServiceSpecialist"
                elif "name='PaymentOpsOrchestrator'" in last_agent_name:
                    agent_name = "PaymentOpsOrchestrator"
                else:
                    agent_name = "PaymentOpsOrchestrator"  # Default fallback

            # Only count as handoff if last_agent is NOT PaymentOpsOrchestrator
            if agent_name == "ComplianceSpecialist":
                handoff_info["agents_involved"].append("ComplianceSpecialist")
                handoff_info["handoffs"].append({
                    "target_agent": "ComplianceSpecialist",
                    "detection_method": "last_agent_field",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                handoff_info["decision_points"].append("Handoff to ComplianceSpecialist")

            elif agent_name == "CustomerServiceSpecialist":
                handoff_info["agents_involved"].append("CustomerServiceSpecialist")
                handoff_info["handoffs"].append({
                    "target_agent": "CustomerServiceSpecialist",
                    "detection_method": "last_agent_field",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                handoff_info["decision_points"].append("Handoff to CustomerServiceSpecialist")

            # If last_agent is PaymentOpsOrchestrator, it means NO handoff occurred
            # In this case, handoff_info remains with just PaymentOpsOrchestrator

        return handoff_info

    def _extract_payment_ids_from_structured_response(self, response) -> list[str]:
        """Extract payment IDs from structured response with fallback"""
        try:
            # Try to get structured output directly
            if hasattr(response, 'parsed_output') and response.parsed_output:
                structured_data = response.parsed_output
                if isinstance(structured_data, PendingPaymentsList):
                    payment_ids = structured_data.payment_ids
                    print(
                        f"✅ [ORCHESTRATOR] Got {len(payment_ids)} "
                        "payment IDs from structured output"
                    )
                    print(f"💳 [ORCHESTRATOR] Payment IDs: {', '.join(payment_ids)}")
                    return payment_ids

            # Fallback: try to parse from final_output
            if hasattr(response, 'final_output'):
                import json
                try:
                    # Try to parse as JSON
                    json_data = json.loads(response.final_output)
                    if 'payment_ids' in json_data:
                        payment_ids = json_data['payment_ids']
                        print(
                            f"✅ [ORCHESTRATOR] Got {len(payment_ids)} "
                            "payment IDs from JSON fallback"
                        )
                        return payment_ids
                except json.JSONDecodeError:
                    pass

            # Last resort: use test payment IDs for consistency
            payment_ids = ["PAY-12345", "PAY-12346", "PAY-12347", "PAY-12348", "PAY-12349"]
            print(
                "⚠️  [ORCHESTRATOR] Could not extract payment IDs from response, "
                f"using test data ({len(payment_ids)} payments)"
            )
            return payment_ids

        except Exception as e:
            print(f"❌ [ORCHESTRATOR] Error extracting payment IDs: {e}")
            # Fallback to test data
            payment_ids = ["PAY-12345", "PAY-12346", "PAY-12347", "PAY-12348", "PAY-12349"]
            print(
                f"⚠️  [ORCHESTRATOR] Using test data fallback "
                f"({len(payment_ids)} payments)"
            )
            return payment_ids

    async def cleanup(self):
        """Clean up all agents and MCP server connection"""
        if not self._initialized:
            return

        try:
            print("🔄 [ORCHESTRATOR] Cleanup initiated")

            # Clear agent references first
            self.primary_agent = None
            self.compliance_agent = None
            self.customer_service_agent = None

            # Clean up MCP server connection
            if self.mcp_server:
                try:
                    await self.mcp_server.cleanup()
                    print("✅ [ORCHESTRATOR] MCP server closed")
                except Exception as e:
                    print(f"⚠️  [ORCHESTRATOR] MCP server close warning: {e}")
                finally:
                    self.mcp_server = None

                # Give async tasks time to finish cleanup gracefully
                import asyncio
                await asyncio.sleep(0.3)

            self._initialized = False
            print("✅ [ORCHESTRATOR] Cleanup complete")

        except Exception as e:
            print(f"⚠️  [ORCHESTRATOR] Cleanup warning: {e}")
            # Always mark as uninitialized even if cleanup had issues
            self._initialized = False

    async def __aenter__(self):
        """Async context manager entry - ensures clean initialization"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with guaranteed cleanup"""
        await self.cleanup()
        # Don't suppress exceptions unless they're cleanup-related
        return False
