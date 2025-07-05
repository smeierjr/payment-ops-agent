"""
Compliance Specialist Agent - Focused on regulatory review and risk assessment
"""

import os
from typing import Dict, Any, Optional
from agents.mcp.server import MCPServerStdio
from agents.agent import Agent
from agents import Runner
from datetime import datetime, timezone

# Compliance specialist instructions
COMPLIANCE_INSTRUCTIONS = """You are a Compliance Specialist focused on regulatory review \
and risk assessment.

CAPABILITIES:
- assess_payment_risk: Detailed risk assessment for specific payments
- get_payment_details: Get detailed payment information for analysis
- escalate_payment: Escalate high-risk payments to human review

FOCUS AREAS:
- AML (Anti-Money Laundering) compliance
- Transaction threshold monitoring
- Risk level assessment (LOW/MEDIUM/HIGH)
- Regulatory reporting requirements

DECISION CRITERIA:
- Amounts >$10,000: Automatically HIGH risk
- International transactions: Enhanced review
- Customer tier considerations (VIP/Business get expedited review)
- Historical compliance patterns

WORKFLOW:
1. Always start with assess_payment_risk for individual payments
2. Use get_payment_details to gather context for analysis
3. Provide clear risk assessments with specific recommendations
4. Document all compliance decisions with detailed reasoning
5. Use escalate_payment for high-risk cases requiring human review

RISK ASSESSMENT FRAMEWORK:
- LOW RISK: Standard processing, routine monitoring
- MEDIUM RISK: Enhanced monitoring, additional documentation
- HIGH RISK: Manual review required, hold processing

Always provide detailed risk assessments and clear recommendations for each payment reviewed."""


class ComplianceSpecialist:
    """
    Compliance Specialist Agent for regulatory review and risk assessment

    This agent handles all compliance-related tasks including AML checks,
    sanctions screening, and high-risk transaction reviews.
    """

    def __init__(self, api_key: Optional[str] = None, mcp_server: Optional[MCPServerStdio] = None):
        """
        Initialize the Compliance Specialist Agent

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            mcp_server: Shared MCP server instance (avoids duplication)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Cost-optimized model
        self.instructions = COMPLIANCE_INSTRUCTIONS

        # Use shared MCP server if provided, otherwise initialize own
        self.mcp_server = mcp_server
        self.agent: Optional[Agent] = None

    async def initialize(self) -> None:
        """Initialize the compliance specialist agent"""
        if not self.mcp_server:
            print("⚠️  [ComplianceSpecialist] Warning: No MCP server provided")
            return

        # Import output guardrails
        from ..guardrails.output_validators import (
            validate_compliance_response,
            validate_sensitive_data_screening,
        )

        # Initialize agent with shared MCP server and output guardrails
        self.agent = Agent(
            name="ComplianceSpecialist",
            instructions=self.instructions,
            model=self.model,
            mcp_servers=[self.mcp_server],
            output_guardrails=[
                validate_compliance_response,
                validate_sensitive_data_screening,
            ],
        )

    async def run(self, message: str) -> Dict[str, Any]:
        """
        Run the compliance specialist with a message

        Args:
            message: Task or query for compliance analysis

        Returns:
            Dict containing compliance analysis results
        """
        if not self.agent:
            await self.initialize()

        if not self.agent:
            return {
                "status": "error",
                "error": "Failed to initialize ComplianceSpecialist",
                "conversation_history": [],
                "final_response": None,
            }

        try:
            # Use the Runner to execute the agent
            runner = Runner()
            response = await runner.run(starting_agent=self.agent, input=message)

            # Extract compliance analysis from response
            compliance_analysis = self._extract_compliance_analysis(response)

            # Format response
            conversation_history = [
                {
                    "turn": 1,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "message": response.final_output,
                    "role": "assistant",
                    "agent": "ComplianceSpecialist",
                    "compliance_analysis": compliance_analysis,
                }
            ]

            result = {
                "status": "completed",
                "agent": "ComplianceSpecialist",
                "total_turns": 1,
                "compliance_summary": {
                    "assessments_performed": compliance_analysis.get("assessments_count", 0),
                    "high_risk_payments": compliance_analysis.get("high_risk_count", 0),
                    "reports_generated": compliance_analysis.get("reports_count", 0),
                    "recommendations": compliance_analysis.get("recommendations", []),
                },
                "conversation_history": conversation_history,
                "final_response": response.final_output,
                "trace_id": getattr(response, "trace_id", None),
            }

            return result

        except Exception as e:
            error_msg = f"Error in ComplianceSpecialist execution: {str(e)}"
            return {
                "status": "error",
                "error": error_msg,
                "conversation_history": [],
                "final_response": None,
            }

    def _extract_compliance_analysis(self, response) -> Dict[str, Any]:
        """Extract compliance analysis from agent response"""
        analysis = {
            "assessments_count": 0,
            "high_risk_count": 0,
            "reports_count": 0,
            "recommendations": [],
        }

        response_str = str(response).lower()

        # Count assessments
        if "assess_payment_risk" in response_str:
            analysis["assessments_count"] = response_str.count("assess_payment_risk")

        # Count high-risk reviews
        if "high_risk" in response_str or "escalate_payment" in response_str:
            analysis["high_risk_count"] = response_str.count("high_risk")

        # Count escalations
        if "escalate_payment" in response_str:
            analysis["reports_count"] = response_str.count("escalate_payment")

        # Extract recommendations
        if "manual review" in response_str:
            analysis["recommendations"].append("Manual review required")
        if "enhanced monitoring" in response_str:
            analysis["recommendations"].append("Enhanced monitoring needed")
        if "hold" in response_str:
            analysis["recommendations"].append("Hold transaction for review")

        return analysis

    async def assess_payment(self, payment_id: str, customer_id: str) -> Dict[str, Any]:
        """
        Assess compliance for a specific payment

        Args:
            payment_id: Payment to assess
            customer_id: Customer making the payment

        Returns:
            Dict containing compliance assessment
        """
        message = f"Assess payment compliance for payment {payment_id} by customer {customer_id}"
        return await self.run(message)

    async def review_high_risk(self, payment_id: str, risk_factors: list) -> Dict[str, Any]:
        """
        Review high-risk transaction

        Args:
            payment_id: Payment to review
            risk_factors: List of identified risk factors

        Returns:
            Dict containing high-risk review results
        """
        risk_factors_str = ", ".join(risk_factors)
        message = f"Review high-risk transaction {payment_id} with risk factors: {risk_factors_str}"
        return await self.run(message)

    async def generate_report(self, payment_ids: list) -> Dict[str, Any]:
        """
        Generate regulatory report for multiple payments

        Args:
            payment_ids: List of payment IDs to include

        Returns:
            Dict containing regulatory report
        """
        payment_ids_str = ", ".join(payment_ids)
        message = f"Generate regulatory report for payments: {payment_ids_str}"
        return await self.run(message)

    async def cleanup(self):
        """Clean up agent (MCP server cleanup handled by orchestrator)"""
        self.agent = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup"""
        await self.cleanup()
        return False
