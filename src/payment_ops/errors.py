"""
Error handling for payment operations agent
Following Mitchell Hashimoto pattern of structured error types
"""


class PaymentOpsError(Exception):
    """Base exception for payment operations errors"""

    pass


class AgentError(PaymentOpsError):
    """Error in agent execution or communication"""

    pass


class MCPError(PaymentOpsError):
    """Error in MCP server communication"""

    pass


class PaymentDataError(PaymentOpsError):
    """Error in payment data access or validation"""

    pass


class ConfigurationError(PaymentOpsError):
    """Error in configuration or environment setup"""

    pass


class CLIError(PaymentOpsError):
    """Error in CLI execution or user interaction"""

    pass
