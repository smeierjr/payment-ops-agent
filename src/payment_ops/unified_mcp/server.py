"""
Payment Operations MCP Server
Provides payment tools for the OpenAI Agent SDK to enable multi-agent workflows.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from fastmcp import FastMCP
from pydantic import BaseModel

try:
    from ..data.mock_payments import mock_db
except ImportError:
    # Fallback for direct script execution
    import sys
    import os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from payment_ops.data.mock_payments import mock_db


class PaymentQueryResponse(BaseModel):
    """Response model for payment queries"""

    payments: List[Dict[str, Any]]
    total_count: int
    timestamp: str


class PaymentDetailsResponse(BaseModel):
    """Response model for payment details"""

    payment: Dict[str, Any]
    timestamp: str


class PaymentActionResponse(BaseModel):
    """Response model for payment actions"""

    action: str
    payment_id: str
    result: str
    details: Dict[str, Any]
    timestamp: str


class RiskAssessmentResponse(BaseModel):
    """Response model for risk assessment"""

    payment_id: str
    risk_level: str
    risk_factors: List[str]
    recommendation: str
    timestamp: str


class NotificationResponse(BaseModel):
    """Response model for customer notifications"""

    notification_id: str
    customer_id: str
    message: str
    channel: str
    status: str
    timestamp: str


# Initialize FastMCP server
mcp_server = FastMCP("payment-ops-server")


@mcp_server.tool()
def get_pending_payments(limit: int = 10) -> PaymentQueryResponse:
    """
    Get pending payments that require attention.

    Args:
        limit: Maximum number of payments to return (default: 10)

    Returns:
        PaymentQueryResponse: List of failed payments needing attention
    """
    failed_payments = mock_db.get_pending_payments()

    # Apply limit
    limited_payments = failed_payments[:limit]

    return PaymentQueryResponse(
        payments=limited_payments,
        total_count=len(failed_payments),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@mcp_server.tool()
def get_payment_details(payment_id: str) -> PaymentDetailsResponse:
    """
    Get detailed information for a specific payment.

    Args:
        payment_id: The payment ID to look up

    Returns:
        PaymentDetailsResponse: Detailed payment information
    """
    payment_details = mock_db.get_payment_details(payment_id)

    return PaymentDetailsResponse(
        payment=payment_details, timestamp=datetime.now(timezone.utc).isoformat()
    )


@mcp_server.tool()
def retry_payment(payment_id: str, reason: str) -> PaymentActionResponse:
    """
    Retry a failed payment with specified reason.

    Args:
        payment_id: The payment ID to retry
        reason: Reason for the retry attempt

    Returns:
        PaymentActionResponse: Result of the retry attempt
    """
    result = mock_db.retry_payment(payment_id, reason)

    return PaymentActionResponse(
        action="RETRY",
        payment_id=payment_id,
        result=result.get("result", "UNKNOWN"),
        details=result,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@mcp_server.tool()
def escalate_payment(payment_id: str, issue_type: str, notes: str) -> PaymentActionResponse:
    """
    Escalate a payment to human review.

    Args:
        payment_id: The payment ID to escalate
        issue_type: Type of issue (e.g., "compliance", "technical", "customer")
        notes: Detailed notes about the issue

    Returns:
        PaymentActionResponse: Result of the escalation
    """
    result = mock_db.escalate_to_human(payment_id, issue_type, notes)

    return PaymentActionResponse(
        action="ESCALATE",
        payment_id=payment_id,
        result="ESCALATED" if "escalation_id" in result else "FAILED",
        details=result,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@mcp_server.tool()
def assess_payment_risk(payment_id: str) -> RiskAssessmentResponse:
    """
    Assess the risk level of a payment for compliance review.

    Args:
        payment_id: The payment ID to assess

    Returns:
        RiskAssessmentResponse: Risk assessment details
    """
    payment = mock_db.get_payment_details(payment_id)

    if "error" in payment:
        return RiskAssessmentResponse(
            payment_id=payment_id,
            risk_level="UNKNOWN",
            risk_factors=["Payment not found"],
            recommendation="Payment ID invalid",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    risk_factors = []
    risk_level = "LOW"

    # Risk assessment logic based on payment attributes
    amount = payment.get("amount", 0)
    customer_tier = payment.get("customer_tier", "standard")
    error_code = payment.get("error_code")

    # High amount risk
    if amount >= 10000:
        risk_factors.append("High transaction amount (>=$10,000)")
        risk_level = "HIGH"
    elif amount >= 3000:
        risk_factors.append("Elevated transaction amount (>=$3,000)")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # Customer tier considerations
    if customer_tier == "vip":
        risk_factors.append("VIP customer - requires special handling")
        if risk_level == "LOW":
            risk_level = "MEDIUM"
    elif customer_tier == "business":
        risk_factors.append("Business account - higher limits")

    # Error code analysis
    if error_code == "COMPLIANCE_HOLD":
        risk_factors.append("Already flagged for compliance review")
        risk_level = "HIGH"
    elif error_code == "UNKNOWN_ERROR":
        risk_factors.append("Unknown error requires investigation")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # International transaction check
    if payment.get("compliance_notes", "").lower().find("international") != -1:
        risk_factors.append("International transaction")
        if risk_level == "LOW":
            risk_level = "MEDIUM"

    # Generate recommendation
    if risk_level == "HIGH":
        recommendation = "Escalate to compliance team for manual review"
    elif risk_level == "MEDIUM":
        recommendation = "Review transaction details before processing"
    else:
        recommendation = "Standard processing acceptable"

    if not risk_factors:
        risk_factors = ["No significant risk factors identified"]

    return RiskAssessmentResponse(
        payment_id=payment_id,
        risk_level=risk_level,
        risk_factors=risk_factors,
        recommendation=recommendation,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@mcp_server.tool()
def notify_customer(
    customer_id: str,
    message: str,
    payment_id: Optional[str] = None,
    channel: str = "email",
) -> NotificationResponse:
    """
    Send notification to customer about payment status.

    Args:
        customer_id: The customer ID to notify
        message: The notification message
        payment_id: Optional payment ID for context
        channel: Communication channel ("email", "sms", "push")

    Returns:
        NotificationResponse: Result of the notification attempt
    """
    # Generate unique notification ID
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    customer_suffix = customer_id.split("-")[-1]
    notification_id = f"NOTIF-{timestamp_str}-{customer_suffix}"

    # Mock notification sending
    success_rate = 0.95  # 95% success rate for notifications
    import random

    status = "SENT" if random.random() < success_rate else "FAILED"

    # In a real implementation, this would be stored in a database
    # For now, we'll just log it to the mock database action log
    mock_db.action_log.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "NOTIFY_CUSTOMER",
            "customer_id": customer_id,
            "payment_id": payment_id,
            "channel": channel,
            "status": status,
            "notification_id": notification_id,
        }
    )

    return NotificationResponse(
        notification_id=notification_id,
        customer_id=customer_id,
        message=message,
        channel=channel,
        status=status,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Tool for debugging/monitoring
@mcp_server.tool()
def get_action_log(limit: int = 20) -> Dict[str, Any]:
    """
    Get recent actions performed by the payment system for debugging.

    Args:
        limit: Maximum number of log entries to return

    Returns:
        Dict containing recent actions and metadata
    """
    actions = mock_db.get_action_log()
    recent_actions = actions[-limit:] if actions else []

    return {
        "actions": recent_actions,
        "total_actions": len(actions),
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "limit": limit,
    }


if __name__ == "__main__":
    # For testing purposes - run the server directly
    print("Starting Payment Operations MCP Server...")
    mcp_server.run()
