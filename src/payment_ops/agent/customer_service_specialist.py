"""
Customer Service Specialist Agent - Focused on payment-related customer communications
"""

import os
from typing import Dict, Any, Optional
from agents.mcp.server import MCPServerStdio, MCPServerStdioParams
from agents.agent import Agent
from agents import Runner
from datetime import datetime, timezone

# Customer service specialist instructions
CUSTOMER_SERVICE_INSTRUCTIONS = """You are a Customer Service Specialist handling \
payment-related customer communications.

CAPABILITIES:
- notify_customer: Send targeted notifications about payment issues
- schedule_customer_outreach: Proactive customer engagement
- handle_customer_inquiry: Respond to payment-related questions

COMMUNICATION PRIORITIES:
- VIP customers: Immediate personal outreach
- Business customers: Dedicated account management approach
- Standard customers: Clear, helpful automated communications

SERVICE LEVELS:
- Critical issues (compliance holds): Same-day resolution
- Payment failures: 24-hour follow-up
- Technical issues: Immediate retry + customer update

WORKFLOW:
1. Identify customer tier and preferred communication method
2. Tailor communication style to customer type and issue severity
3. For VIP/Business customers, always schedule follow-up outreach
4. For standard customers, provide clear self-service options
5. Document all customer interactions with clear next steps

COMMUNICATION TEMPLATES:
- VIP customers: Personal, immediate, with dedicated support
- Business customers: Professional, account-focused, with relationship management
- Standard customers: Clear, helpful, with self-service guidance

Always prioritize customer experience and clear communication. Ensure customers understand:
- What happened with their payment
- What action is being taken
- What they need to do (if anything)
- When they can expect resolution"""


class CustomerServiceSpecialist:
    """
    Customer Service Specialist Agent for handling payment-related customer communications

    This agent is responsible for all customer outreach, notifications, and service recovery.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Customer Service Specialist Agent

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Cost-optimized model
        self.instructions = CUSTOMER_SERVICE_INSTRUCTIONS

        self.agent: Optional[Agent] = None
        self.mcp_server: Optional[MCPServerStdio] = None

    async def initialize(self) -> None:
        """Initialize the customer service specialist agent"""
        await self.setup_mcp_server()

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
            params = MCPServerStdioParams(command="uv", args=["run", "python", mcp_server_path])
            self.mcp_server = MCPServerStdio(params=params)

            # Initialize agent with MCP server
            self.agent = Agent(
                name="CustomerServiceSpecialist",
                instructions=self.instructions,
                model=self.model,  # Cost-optimized model
                mcp_servers=[self.mcp_server],
            )

        except Exception as e:
            print(f"Warning: Failed to setup MCP server for CustomerServiceSpecialist: {e}")
            self.mcp_server = None
            self.agent = None

    async def run(self, message: str) -> Dict[str, Any]:
        """
        Run the customer service specialist with a message

        Args:
            message: Task or query for customer service

        Returns:
            Dict containing customer service results
        """
        if not self.agent:
            await self.initialize()

        if not self.agent:
            return {
                "status": "error",
                "error": "Failed to initialize CustomerServiceSpecialist",
                "conversation_history": [],
                "final_response": None,
            }

        try:
            # Connect to the MCP server
            if self.mcp_server is not None:
                await self.mcp_server.connect()

            # Use the Runner to execute the agent
            if self.agent is not None:
                runner = Runner()
                response = await runner.run(starting_agent=self.agent, input=message)
            else:
                raise RuntimeError("CustomerServiceSpecialist agent not initialized")

            # Extract customer service analysis from response
            service_analysis = self._extract_service_analysis(response)

            # Format response
            conversation_history = [
                {
                    "turn": 1,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "message": response.final_output,
                    "role": "assistant",
                    "agent": "CustomerServiceSpecialist",
                    "service_analysis": service_analysis,
                }
            ]

            result = {
                "status": "completed",
                "agent": "CustomerServiceSpecialist",
                "total_turns": 1,
                "service_summary": {
                    "notifications_sent": service_analysis.get("notifications_count", 0),
                    "outreach_scheduled": service_analysis.get("outreach_count", 0),
                    "inquiries_handled": service_analysis.get("inquiries_count", 0),
                    "customers_contacted": service_analysis.get("customers_contacted", []),
                    "service_level": service_analysis.get("service_level", "standard"),
                },
                "conversation_history": conversation_history,
                "final_response": response.final_output,
                "trace_id": getattr(response, "trace_id", None),
            }

            return result

        except Exception as e:
            error_msg = f"Error in CustomerServiceSpecialist execution: {str(e)}"
            return {
                "status": "error",
                "error": error_msg,
                "conversation_history": [],
                "final_response": None,
            }

    def _extract_service_analysis(self, response) -> Dict[str, Any]:
        """Extract customer service analysis from agent response"""
        analysis = {
            "notifications_count": 0,
            "outreach_count": 0,
            "inquiries_count": 0,
            "customers_contacted": [],
            "service_level": "standard",
        }

        response_str = str(response).lower()

        # Count notifications
        if "notify_customer" in response_str:
            analysis["notifications_count"] = response_str.count("notify_customer")

        # Count outreach scheduling
        if "schedule_customer_outreach" in response_str:
            analysis["outreach_count"] = response_str.count("schedule_customer_outreach")

        # Count inquiries handled
        if "handle_customer_inquiry" in response_str:
            analysis["inquiries_count"] = response_str.count("handle_customer_inquiry")

        # Determine service level
        if "vip" in response_str:
            analysis["service_level"] = "vip"
        elif "business" in response_str:
            analysis["service_level"] = "business"

        # Extract customer IDs if mentioned
        import re

        customer_ids = re.findall(r"CUST-\d+", str(response))
        analysis["customers_contacted"] = list(set(customer_ids))

        return analysis

    async def notify_customer(
        self,
        customer_id: str,
        payment_id: str,
        issue_type: str,
        message_template: str = "default",
    ) -> Dict[str, Any]:
        """
        Send notification to customer about payment issue

        Args:
            customer_id: Customer to notify
            payment_id: Related payment ID
            issue_type: Type of issue
            message_template: Template to use

        Returns:
            Dict containing notification results
        """
        message = (
            f"Send {message_template} notification to customer {customer_id} "
            f"about payment {payment_id} with issue type: {issue_type}"
        )
        return await self.run(message)

    async def schedule_outreach(
        self,
        customer_id: str,
        outreach_type: str,
        priority: str = "normal",
        days_delay: int = 3,
    ) -> Dict[str, Any]:
        """
        Schedule proactive customer outreach

        Args:
            customer_id: Customer to reach out to
            outreach_type: Type of outreach
            priority: Outreach priority
            days_delay: Days to wait before outreach

        Returns:
            Dict containing scheduled outreach details
        """
        message = (
            f"Schedule {priority} priority {outreach_type} outreach "
            f"for customer {customer_id} in {days_delay} days"
        )
        return await self.run(message)

    async def handle_inquiry(
        self, customer_id: str, inquiry_type: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle customer inquiry about payment issues

        Args:
            customer_id: Customer making the inquiry
            inquiry_type: Type of inquiry
            context: Additional context

        Returns:
            Dict containing inquiry response
        """
        context_str = ", ".join([f"{k}: {v}" for k, v in context.items()])
        message = (
            f"Handle {inquiry_type} inquiry from customer {customer_id} "
            f"with context: {context_str}"
        )
        return await self.run(message)

    async def cleanup(self):
        """Clean up MCP server connection"""
        try:
            if self.mcp_server:
                print("CustomerServiceSpecialist cleanup initiated")
                # Give a moment for natural cleanup
                import asyncio

                await asyncio.sleep(0.1)
                self.mcp_server = None
            self.agent = None
        except Exception:
            # Suppress cleanup errors to avoid noise
            pass

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup"""
        await self.cleanup()
        return False
