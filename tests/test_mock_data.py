"""
Tests for mock payment data
"""

import sys
from pathlib import Path

from src.payment_ops.data.mock_payments import MockPaymentDatabase, MOCK_PAYMENTS, mock_db

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestMockPaymentDatabase:
    """Test suite for MockPaymentDatabase"""

    def setup_method(self):
        """Setup fresh database for each test"""
        self.db = MockPaymentDatabase()
        self.db.reset_data()
        # Also reset the global instance to avoid pollution
        mock_db.reset_data()

    def teardown_method(self):
        """Clean up after each test"""
        if hasattr(self, "db"):
            self.db.reset_data()
        # Also reset the global instance
        mock_db.reset_data()

    def test_action_log(self):
        """Test action logging"""
        # Verify initial state
        assert len(self.db.get_action_log()) == 0

        # Perform some actions
        retry_result = self.db.retry_payment("PAY-12346", "Test retry")
        escalate_result = self.db.escalate_to_human("PAY-12347", "TEST", "Test escalation")

        # Both should succeed
        assert "error" not in retry_result
        assert "error" not in escalate_result

        # Check log
        log = self.db.get_action_log()
        assert len(log) == 2

        # Check retry log entry
        retry_entry = next(e for e in log if e["action"] == "RETRY")
        assert retry_entry["payment_id"] == "PAY-12346"
        assert retry_entry["reason"] == "Test retry"

        # Check escalation log entry
        escalation_entry = next(e for e in log if e["action"] == "ESCALATE")
        assert escalation_entry["payment_id"] == "PAY-12347"
        assert escalation_entry["issue_type"] == "TEST"

    def test_get_pending_payments(self):
        """Test getting pending payments"""
        pending = self.db.get_pending_payments()

        # Should return only FAILED payments
        assert all(p["status"] == "FAILED" for p in pending)

        # Should return at most 10 payments
        assert len(pending) <= 10

        # Should have expected payment IDs (respecting the 10 payment limit)
        expected_failed = [p for p in MOCK_PAYMENTS if p["status"] == "FAILED"]
        assert len(pending) == min(len(expected_failed), 10)

    def test_get_payment_details_valid(self):
        """Test getting details for valid payment"""
        payment = self.db.get_payment_details("PAY-12345")

        assert "error" not in payment
        assert payment["payment_id"] == "PAY-12345"
        assert payment["amount"] == 1500.00
        assert payment["status"] == "FAILED"

    def test_get_payment_details_invalid(self):
        """Test getting details for invalid payment"""
        payment = self.db.get_payment_details("PAY-INVALID")

        assert "error" in payment
        assert "not found" in payment["error"].lower()

    def test_retry_payment_success(self):
        """Test successful payment retry"""
        # Use PAY-12349 which has retry_count 1, but reset it for this test
        payment = self.db.get_payment_details("PAY-12349")
        # Reset it to FAILED status for testing
        payment["status"] = "FAILED"
        payment["retry_count"] = 0

        assert payment["status"] == "FAILED"
        original_retry_count = payment["retry_count"]

        # Retry the payment
        result = self.db.retry_payment("PAY-12349", "Test retry")

        assert "error" not in result
        assert result["action"] == "RETRY"
        assert result["retry_count"] == original_retry_count + 1

        # Check payment was updated
        updated_payment = self.db.get_payment_details("PAY-12349")
        assert updated_payment["retry_count"] == original_retry_count + 1

    def test_escalate_payment(self):
        """Test payment escalation"""
        result = self.db.escalate_to_human(
            "PAY-12345", "INSUFFICIENT_FUNDS", "Customer needs new payment method"
        )

        assert "error" not in result
        assert result["action"] == "ESCALATE"
        assert result["issue_type"] == "INSUFFICIENT_FUNDS"
        assert "ESC-" in result["escalation_id"]

        # Check payment status was updated
        payment = self.db.get_payment_details("PAY-12345")
        assert payment["status"] == "ESCALATED"
