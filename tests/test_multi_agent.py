#!/usr/bin/env python3
"""
Tests for multi-agent system functionality
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestMultiAgentIntegration:
    """Test integration between agents"""

    def test_payment_ops_orchestrator_import(self):
        """Test that payment ops orchestrator works"""
        from src.payment_ops.agent.payment_ops_orchestrator import PaymentOpsOrchestrator

        orchestrator = PaymentOpsOrchestrator()
        assert orchestrator is not None
        assert hasattr(orchestrator, 'run')
        assert hasattr(orchestrator, 'cleanup')

    def test_project_structure_integrity(self):
        """Test that project structure supports multi-agent system"""
        # Check that all required directories exist
        unified_mcp_dir = project_root / "src" / "payment_ops" / "unified_mcp"
        agent_dir = project_root / "src" / "payment_ops" / "agent"

        assert unified_mcp_dir.exists()
        assert agent_dir.exists()

        # Check that __init__.py files exist
        assert (unified_mcp_dir / "__init__.py").exists()
        assert (agent_dir / "__init__.py").exists()

    def test_error_handling_imports(self):
        """Test that error handling still works with multi-agent system"""
        from src.payment_ops.errors import PaymentOpsError

        # Should be able to create error
        error = PaymentOpsError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
