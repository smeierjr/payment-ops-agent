"""
Mock payment data for testing the Payment Operations Agent
"""

from datetime import datetime, timezone
from typing import List, Dict, Any
import random

# Mock payment data following PRD schema
MOCK_PAYMENTS = [
    # Original payments (keep for compatibility)
    {
        "payment_id": "PAY-12345",
        "amount": 1500.00,
        "status": "FAILED",
        "error_code": "INSUFFICIENT_FUNDS",
        "retry_count": 0,
        "last_attempt": "2025-06-15T10:30:00Z",
        "customer_id": "CUST-789",
        "customer_tier": "standard",
        "description": "Monthly subscription payment",
        "created_at": "2025-06-15T10:29:45Z",
    },
    {
        "payment_id": "PAY-12346",
        "amount": 250.00,
        "status": "FAILED",
        "error_code": "TECHNICAL_FAILURE",
        "retry_count": 0,
        "last_attempt": "2025-06-27T14:15:00Z",
        "customer_id": "CUST-790",
        "customer_tier": "standard",
        "description": "One-time purchase",
        "created_at": "2025-06-27T14:14:30Z",
    },
    {
        "payment_id": "PAY-12347",
        "amount": 3200.00,
        "status": "FAILED",
        "error_code": "COMPLIANCE_HOLD",
        "retry_count": 0,
        "last_attempt": "2025-06-26T09:45:00Z",
        "customer_id": "CUST-791",
        "customer_tier": "standard",
        "description": "High-value transaction",
        "created_at": "2025-06-26T09:44:15Z",
    },
    {
        "payment_id": "PAY-12348",
        "amount": 75.00,
        "status": "FAILED",
        "error_code": "CARD_DECLINED",
        "retry_count": 2,
        "last_attempt": "2025-06-25T16:20:00Z",
        "customer_id": "CUST-792",
        "customer_tier": "standard",
        "description": "Small purchase",
        "created_at": "2025-06-25T16:18:00Z",
    },
    {
        "payment_id": "PAY-12349",
        "amount": 890.00,
        "status": "FAILED",
        "error_code": "TECHNICAL_FAILURE",
        "retry_count": 1,
        "last_attempt": "2025-06-20T11:30:00Z",
        "customer_id": "CUST-793",
        "customer_tier": "standard",
        "description": "Service payment",
        "created_at": "2025-06-20T11:29:00Z",
    },
    {
        "payment_id": "PAY-12350",
        "amount": 120.00,
        "status": "PENDING",
        "error_code": None,
        "retry_count": 0,
        "last_attempt": "2025-06-28T08:00:00Z",
        "customer_id": "CUST-794",
        "customer_tier": "standard",
        "description": "Processing payment",
        "created_at": "2025-06-28T07:59:30Z",
    },
    # Enhanced scenarios for better multi-agent testing
    # VIP customers with special handling requirements
    {
        "payment_id": "PAY-13001",
        "amount": 4500.00,
        "status": "FAILED",
        "error_code": "INSUFFICIENT_FUNDS",
        "retry_count": 0,
        "last_attempt": "2025-06-28T15:30:00Z",
        "customer_id": "CUST-VIP-001",
        "customer_tier": "vip",
        "description": "VIP premium service payment",
        "created_at": "2025-06-28T15:29:00Z",
    },
    {
        "payment_id": "PAY-13002",
        "amount": 12500.00,
        "status": "FAILED",
        "error_code": "COMPLIANCE_HOLD",
        "retry_count": 0,
        "last_attempt": "2025-06-28T16:00:00Z",
        "customer_id": "CUST-VIP-002",
        "customer_tier": "vip",
        "description": "VIP large transaction",
        "created_at": "2025-06-28T15:58:00Z",
    },
    # Borderline compliance cases
    {
        "payment_id": "PAY-13003",
        "amount": 2999.00,
        "status": "FAILED",
        "error_code": "COMPLIANCE_HOLD",
        "retry_count": 0,
        "last_attempt": "2025-06-28T12:00:00Z",
        "customer_id": "CUST-850",
        "customer_tier": "standard",
        "description": "Borderline high-value purchase",
        "created_at": "2025-06-28T11:58:00Z",
        "compliance_notes": "Just under $3000 threshold, review recommended",
    },
    {
        "payment_id": "PAY-13004",
        "amount": 5000.00,
        "status": "FAILED",
        "error_code": "UNKNOWN_ERROR",
        "retry_count": 0,
        "last_attempt": "2025-06-28T13:15:00Z",
        "customer_id": "CUST-851",
        "customer_tier": "standard",
        "description": "Unusual error requiring investigation",
        "created_at": "2025-06-28T13:14:00Z",
        "compliance_notes": "Unknown error on high-value transaction",
    },
    # Multiple retry scenarios
    {
        "payment_id": "PAY-13005",
        "amount": 450.00,
        "status": "FAILED",
        "error_code": "TECHNICAL_FAILURE",
        "retry_count": 0,
        "last_attempt": "2025-06-29T08:00:00Z",
        "customer_id": "CUST-852",
        "customer_tier": "standard",
        "description": "Fresh technical failure - retry eligible",
        "created_at": "2025-06-29T07:58:00Z",
    },
    {
        "payment_id": "PAY-13006",
        "amount": 325.00,
        "status": "FAILED",
        "error_code": "TECHNICAL_FAILURE",
        "retry_count": 1,
        "last_attempt": "2025-06-28T14:00:00Z",
        "customer_id": "CUST-853",
        "customer_tier": "standard",
        "description": "Technical failure - at retry limit",
        "created_at": "2025-06-28T13:58:00Z",
    },
    # Business customer scenarios
    {
        "payment_id": "PAY-13007",
        "amount": 8750.00,
        "status": "FAILED",
        "error_code": "COMPLIANCE_HOLD",
        "retry_count": 0,
        "last_attempt": "2025-06-28T10:30:00Z",
        "customer_id": "CUST-BIZ-001",
        "customer_tier": "business",
        "description": "B2B invoice payment",
        "created_at": "2025-06-28T10:28:00Z",
        "compliance_notes": "Business account, higher threshold",
    },
    {
        "payment_id": "PAY-13008",
        "amount": 2250.00,
        "status": "FAILED",
        "error_code": "INSUFFICIENT_FUNDS",
        "retry_count": 0,
        "last_attempt": "2025-06-28T11:45:00Z",
        "customer_id": "CUST-BIZ-002",
        "customer_tier": "business",
        "description": "Business subscription renewal",
        "created_at": "2025-06-28T11:43:00Z",
    },
    # International/complex scenarios
    {
        "payment_id": "PAY-13009",
        "amount": 1875.00,
        "status": "FAILED",
        "error_code": "CARD_DECLINED",
        "retry_count": 1,
        "last_attempt": "2025-06-28T09:15:00Z",
        "customer_id": "CUST-INTL-001",
        "customer_tier": "standard",
        "description": "International card payment",
        "created_at": "2025-06-28T09:13:00Z",
        "compliance_notes": "International transaction",
    },
    {
        "payment_id": "PAY-13010",
        "amount": 15000.00,
        "status": "FAILED",
        "error_code": "COMPLIANCE_HOLD",
        "retry_count": 0,
        "last_attempt": "2025-06-28T14:30:00Z",
        "customer_id": "CUST-INTL-002",
        "customer_tier": "vip",
        "description": "Large international transfer",
        "created_at": "2025-06-28T14:28:00Z",
        "compliance_notes": "High-value international, requires enhanced review",
    },
    # Edge cases for agent decision making
    {
        "payment_id": "PAY-13011",
        "amount": 99.99,
        "status": "FAILED",
        "error_code": "COMPLIANCE_HOLD",
        "retry_count": 0,
        "last_attempt": "2025-06-28T16:45:00Z",
        "customer_id": "CUST-854",
        "customer_tier": "standard",
        "description": "Small amount compliance hold (unusual)",
        "created_at": "2025-06-28T16:43:00Z",
        "compliance_notes": "Small transaction flagged - investigate pattern",
    },
    {
        "payment_id": "PAY-13012",
        "amount": 750.00,
        "status": "FAILED",
        "error_code": "INSUFFICIENT_FUNDS",
        "retry_count": 1,
        "last_attempt": "2025-06-27T17:00:00Z",
        "customer_id": "CUST-855",
        "customer_tier": "standard",
        "description": "Insufficient funds after retry",
        "created_at": "2025-06-27T16:58:00Z",
    },
    # Time-sensitive scenarios
    {
        "payment_id": "PAY-13013",
        "amount": 425.00,
        "status": "FAILED",
        "error_code": "TECHNICAL_FAILURE",
        "retry_count": 0,
        "last_attempt": "2025-06-29T06:00:00Z",
        "customer_id": "CUST-856",
        "customer_tier": "standard",
        "description": "Recent failure - immediate retry eligible",
        "created_at": "2025-06-29T05:58:00Z",
    },
    {
        "payment_id": "PAY-13014",
        "amount": 1200.00,
        "status": "FAILED",
        "error_code": "TECHNICAL_FAILURE",
        "retry_count": 0,
        "last_attempt": "2025-06-26T08:00:00Z",
        "customer_id": "CUST-857",
        "customer_tier": "standard",
        "description": "Older technical failure",
        "created_at": "2025-06-26T07:58:00Z",
    },
    # Customer communication variety
    {
        "payment_id": "PAY-13015",
        "amount": 350.00,
        "status": "FAILED",
        "error_code": "CARD_DECLINED",
        "retry_count": 0,
        "last_attempt": "2025-06-28T18:30:00Z",
        "customer_id": "CUST-858",
        "customer_tier": "standard",
        "description": "First-time card decline",
        "created_at": "2025-06-28T18:28:00Z",
    },
]


class MockPaymentDatabase:
    """
    Mock payment database for testing
    """

    def __init__(self):
        self.payments = MOCK_PAYMENTS.copy()
        self.action_log = []

    def get_pending_payments(self) -> List[Dict[str, Any]]:
        """
        Get all payments that need attention (FAILED status)
        """
        failed_payments = [p for p in self.payments if p["status"] == "FAILED"]
        return failed_payments[:10]  # Limit to 10 as per PRD

    def get_payment_details(self, payment_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific payment
        """
        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                return payment
        return {"error": f"Payment {payment_id} not found"}

    def retry_payment(self, payment_id: str, reason: str) -> Dict[str, Any]:
        """
        Simulate retrying a payment
        """
        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                if payment["status"] != "FAILED":
                    return {"error": f"Payment {payment_id} is not in FAILED status"}

                # Simulate retry logic
                payment["retry_count"] += 1
                payment["last_attempt"] = datetime.now(timezone.utc).isoformat()

                # 70% success rate for retries
                if random.random() < 0.7:
                    payment["status"] = "COMPLETED"
                    result = "SUCCESS"
                else:
                    result = "FAILED"

                # Log the action
                self.action_log.append(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "action": "RETRY",
                        "payment_id": payment_id,
                        "reason": reason,
                        "result": result,
                        "retry_count": payment["retry_count"],
                    }
                )

                return {
                    "payment_id": payment_id,
                    "action": "RETRY",
                    "result": result,
                    "retry_count": payment["retry_count"],
                    "reason": reason,
                }

        return {"error": f"Payment {payment_id} not found"}

    def escalate_to_human(self, payment_id: str, issue_type: str, notes: str) -> Dict[str, Any]:
        """
        Simulate escalating a payment to human review
        """
        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                # Log the escalation
                self.action_log.append(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "action": "ESCALATE",
                        "payment_id": payment_id,
                        "issue_type": issue_type,
                        "notes": notes,
                        "amount": payment["amount"],
                    }
                )

                # Update payment status
                payment["status"] = "ESCALATED"

                return {
                    "payment_id": payment_id,
                    "action": "ESCALATE",
                    "issue_type": issue_type,
                    "notes": notes,
                    "escalation_id": f"ESC-{payment_id.split('-')[1]}",
                    "status": "ESCALATED",
                }

        return {"error": f"Payment {payment_id} not found"}

    def get_action_log(self) -> List[Dict[str, Any]]:
        """
        Get the complete action log for audit purposes
        """
        return self.action_log.copy()

    def reset_data(self) -> None:
        """
        Reset to original mock data (useful for testing)
        """
        self.payments = MOCK_PAYMENTS.copy()
        self.action_log = []


# Global instance for easy access
mock_db = MockPaymentDatabase()
