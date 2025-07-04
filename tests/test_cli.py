"""
Tests for CLI functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import CLI functions (we'll need to refactor the CLI to be more testable)
# For now, test the core functionality


class TestCLICore:
    """Test core CLI functionality"""

    def test_project_structure(self):
        """Test that project structure is correct"""
        project_root = Path(__file__).parent.parent

        # Check required directories exist
        assert (project_root / "src").exists()
        assert (project_root / "src" / "payment_ops").exists()
        assert (project_root / "src" / "payment_ops" / "agent").exists()
        assert (project_root / "src" / "payment_ops" / "unified_mcp").exists()
        assert (project_root / "src" / "payment_ops" / "data").exists()
        assert (project_root / "tests").exists()

        # Check required files exist
        assert (project_root / "src" / "payment_ops" / "cli.py").exists()
        orchestrator_path = (project_root / "src" / "payment_ops" / "agent"
                             / "payment_ops_orchestrator.py")
        assert orchestrator_path.exists()
        assert (project_root / "src" / "payment_ops" / "unified_mcp" / "server.py").exists()
        assert (project_root / "src" / "payment_ops" / "data" / "mock_payments.py").exists()

    def test_imports_work(self):
        """Test that all imports work correctly"""
        # Test orchestrator import
        from src.payment_ops.agent.payment_ops_orchestrator import PaymentOpsOrchestrator

        assert PaymentOpsOrchestrator is not None

        # Test data import
        from src.payment_ops.data.mock_payments import mock_db

        assert mock_db is not None

        # Test errors import
        from src.payment_ops.errors import PaymentOpsError, AgentError

        assert PaymentOpsError is not None
        assert AgentError is not None
