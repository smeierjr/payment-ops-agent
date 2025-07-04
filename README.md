# Payment Operations Agent - Multi-Agent System

A production-ready multi-agent CLI application for automated payment operations using OpenAI's Agent SDK and Model Context Protocol (MCP). Built for developers who need to understand both AI agent patterns and real-world payment processing workflows.

## Overview

This project demonstrates modern multi-agent AI architecture through a practical payment operations use case. The system coordinates between specialized agents (Payment Operations, Customer Service, and Compliance) to handle failed payments with comprehensive workflow automation.

**Key Features:**
- **Multi-Agent Architecture**: Coordinated specialist agents with handoff patterns
- **MCP Protocol**: Standards-compliant tool integration across all agents
- **Production CLI**: Clean, professional terminal interface with multi-agent commands
- **Cost Optimized**: Uses GPT-4o-mini for ~85% cost savings
- **Business Logic**: Real payment operations, compliance, and customer service workflows
- **Full Traceability**: Complete audit trail of all actions and agent handoffs

## Architecture

```
┌─────────────────┐                    ┌─────────────────────────┐
│   CLI Interface │ ──────────────────►│  Multi-Agent Coordinator│
│ (Enhanced CLI)  │                    │  (Workflow Orchestrator)│
└─────────────────┘                    └─────────┬───────────────┘
                                                 │
                          ┌──────────────────────┼──────────────────────┐
                          ▼                      ▼                      ▼
               ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
               │ Payment Ops     │    │ Customer Service│    │ Compliance      │
               │ Agent           │    │ Agent           │    │ Agent           │
               └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
                         │ MCP                  │ MCP                  │ MCP
                         ▼                      ▼                      ▼
               ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
               │ Payment MCP     │    │ Customer MCP    │    │ Compliance MCP  │
               │ Server          │    │ Server          │    │ Server          │
               └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Technology Stack:**
- **Agent Framework**: OpenAI Agents SDK with multi-agent coordination
- **Tool Protocol**: Model Context Protocol (MCP) with multiple servers
- **CLI Framework**: Pure Python with multi-agent command support
- **Package Manager**: UV for fast, reliable dependency management
- **Model**: GPT-4o-mini for cost-effective operations
- **Architecture**: Coordinated specialist agents with handoff patterns

## Quick Start

### Prerequisites

- Python 3.11+
- [UV package manager](https://docs.astral.sh/uv/)
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd payment-ops-agent

# Install dependencies
uv sync

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Basic Usage

**⚠️ Important**: Always run from the project root directory to avoid import path issues.

```bash
# Recommended methods (from project root):

# 1. Using UV entry point (recommended)
uv run payment-ops -q "analyze pending payments"  # Single agent
uv run payment-ops  # Interactive mode with multi-agent commands

# 2. Using development scripts
./scripts/dev run -q "analyze pending payments"
./scripts/dev run  # Interactive mode

# Show help
uv run payment-ops --help

# ❌ Don't run directly (causes import errors):
# python src/payment_ops/cli.py
```

## CLI Interface

The CLI provides both single-shot and interactive modes designed for daily operations.

### Interactive Mode

```bash
$ uv run payment-ops
================================================================================
🤖 Payment Operations CLI - Multi-Agent System
================================================================================
Commands: analyze, multi-agent, compliance, customer-service, help, history, exit

payment-ops> multi-agent
🚀 Starting Multi-Agent Workflow...
   📊 Phase 1: Payment Operations Analysis
   🔍 Phase 2: Compliance Assessment
   📞 Phase 3: Customer Service Communications

🚀 Multi-Agent Payment Operations Summary
==========================================================================================

📊 Payment Operations (5 payments processed)
--------------------------------------------------
1. PAY-12345: Insufficient funds → escalate
2. PAY-12346: Technical failure → retry
3. PAY-12347: Compliance hold → escalate
4. PAY-12348: Card declined → no action
5. PAY-12349: Technical failure → no action

🔍 Compliance Assessment (2 reviews)
--------------------------------------------------
• PAY-12345: Risk Level MEDIUM
• PAY-12347: Risk Level HIGH

📞 Customer Service (3 communications)
--------------------------------------------------
• PAY-12345: Customer notified about insufficient_funds
• PAY-12346: Customer notified about technical_failure
• PAY-12347: Customer notified about compliance_hold

📈 Workflow Summary
--------------------------------------------------
Total Payments: 5
Handoffs Completed: 5
Agents Involved: payment_ops, compliance, customer_service
==========================================================================================

payment-ops> compliance PAY-12345
🔍 Running Compliance Assessment...
🔍 Compliance Assessment Results
============================================================
Payment: PAY-12345
Risk Level: MEDIUM
Recommendations: Enhanced monitoring recommended, Manual review required for high-value transactions
============================================================

payment-ops> customer-service notify PAY-12345
📞 Running Customer Service Actions...
📞 Customer Service Results
============================================================
Payment: PAY-12345
Customer: CUST-789
Action: Customer service agent completed communication tasks
============================================================

payment-ops> exit
👋 Goodbye!
```

### Available Commands

**Single Agent Commands:**
- **`analyze`** - Analyze pending payments (single agent mode)

**Multi-Agent Commands:**
- **`multi-agent`** - Run comprehensive 3-phase workflow (Payment Ops → Compliance → Customer Service)
- **`compliance [payment_id]`** - Run compliance-only assessment
- **`customer-service [action] [payment_id]`** - Run customer service actions

**Utility Commands:**
- **`help`** - Show command help and examples  
- **`history`** - View previous analysis results with timestamps
- **`clear`** - Clear terminal screen
- **`exit`** - Exit the CLI

### Single Query Mode

For automation and scripting:

```bash
# Single agent analysis
uv run payment-ops -q "analyze pending payments"

# Multi-agent workflows (interactive mode recommended)
uv run payment-ops  # Then use: multi-agent, compliance, customer-service

# Custom analysis queries
uv run payment-ops -q "what payments need attention?"
uv run payment-ops -q "retry failed technical payments"
```

## Business Logic

The multi-agent system implements realistic payment operations workflows:

### Payment Operations Agent
- **Insufficient Funds** → Escalate with customer notification
- **Technical Failure** → Retry once if < 24 hours old, else escalate
- **Compliance Hold** → Escalate to compliance team
- **Card Declined** → Escalate after retry limit exceeded
- **Unknown Errors** → Escalate with full context

### Compliance Agent
- **AML Compliance Checks** → Risk scoring and assessment
- **Sanctions Screening** → Customer watchlist verification
- **Risk Assessment** → LOW/MEDIUM/HIGH risk classification
- **Case Creation** → Manual review for high-risk transactions
- **Regulatory Reporting** → Comprehensive compliance documentation

### Customer Service Agent
- **Customer Notifications** → Automated communication about payment issues
- **Contact Preferences** → Email/phone preference management
- **Follow-up Scheduling** → Automated customer outreach planning
- **Communication History** → Complete interaction tracking

### Multi-Agent Coordination
- **Phase 1**: Payment Operations analysis and initial actions
- **Phase 2**: Compliance assessment for escalated payments
- **Phase 3**: Customer Service notifications for all failed payments
- **Handoff Tracking**: Complete audit trail of agent interactions

### Mock Data

The system includes realistic test data with 5 failed payments covering different scenarios:

```python
{
    "payment_id": "PAY-12345",
    "amount": 1500.00,
    "status": "FAILED", 
    "error_code": "INSUFFICIENT_FUNDS",
    "retry_count": 0,
    "last_attempt": "2025-06-15T10:30:00Z",
    "customer_id": "CUST-789"
}
```

## Development

### Project Structure

```
payment-ops-agent/
├── src/
│   └── payment_ops/                # Main package
│       ├── __init__.py             # Package initialization
│       ├── cli.py                  # Enhanced CLI with multi-agent support
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── payment_ops.py      # Payment Operations Agent
│       │   ├── customer_service.py # Customer Service Agent
│       │   ├── compliance.py       # Compliance Agent
│       │   └── multi_agent_coordinator.py # Multi-Agent Coordinator
│       ├── payment_mcp/
│       │   ├── __init__.py
│       │   └── server.py           # Payment operations MCP tools
│       ├── customer_mcp/
│       │   ├── __init__.py
│       │   └── server.py           # Customer service MCP tools
│       ├── compliance_mcp/
│       │   ├── __init__.py
│       │   └── server.py           # Compliance MCP tools
│       ├── data/
│       │   ├── __init__.py
│       │   └── mock_payments.py    # Test payment data
│       └── errors.py               # Error handling
├── tests/                          # Test suite
│   ├── test_mock_data.py
│   ├── test_cli.py
│   └── test_multi_agent.py         # Multi-agent system tests
├── scripts/                        # Development scripts
│   ├── dev                         # Development helper
│   └── test                        # Test runner
└── pyproject.toml                  # Project configuration
```

### Key Components

**Multi-Agent Coordinator** (`src/payment_ops/agent/multi_agent_coordinator.py`):
- Orchestrates workflows between all agents
- Manages agent handoffs and communication
- Tracks inter-agent coordination and audit trails
- Provides comprehensive workflow summaries

**Payment Operations Agent** (`src/payment_ops/agent/payment_ops.py`):
- Core payment analysis and decision logic
- Implements payment business rules
- Manages payment operations MCP tools

**Customer Service Agent** (`src/payment_ops/agent/customer_service.py`):
- Handles customer communication and notifications
- Manages contact preferences and history
- Schedules follow-ups and tracks interactions

**Compliance Agent** (`src/payment_ops/agent/compliance.py`):
- Conducts AML compliance checks and risk assessment
- Performs sanctions screening and regulatory compliance
- Creates compliance cases and generates reports

**MCP Servers**:
- **Payment MCP** (`src/payment_ops/payment_mcp/server.py`): Payment operations tools
- **Customer MCP** (`src/payment_ops/customer_mcp/server.py`): Customer service tools
- **Compliance MCP** (`src/payment_ops/compliance_mcp/server.py`): Compliance and risk tools

**Enhanced CLI Interface** (`src/payment_ops/cli.py`):
- Multi-agent workflow commands
- Individual agent access (compliance, customer-service)
- Session history with multi-agent result storage
- Professional terminal interface with no complex dependencies

### Development Scripts

The project provides two optimized scripts for different development workflows:

#### `./scripts/test` - Primary Validation Script
**Use this after making code changes** - your main quality gate:

```bash
# Run complete validation suite (fast & comprehensive)
./scripts/test

# Includes:
# ✅ All 26 pytest tests 
# ✅ Flake8 linting (code style, line length, unused imports)
# ✅ Python syntax check (optimized for speed)
# ✅ Dependency verification

# Expected completion time: ~30 seconds
```

#### `./scripts/dev` - Development Utilities
**Use for individual development tasks** during coding:

```bash
# Show available commands
./scripts/dev help

# Quick CLI testing (without full test suite)
./scripts/dev run -q "analyze pending payments"     # Single query
./scripts/dev run                                   # Interactive mode

# Individual development tasks
./scripts/dev lint                                  # Just linting (subset of ./scripts/test)
./scripts/dev format                                # Auto-format code with black
./scripts/dev server                                # Start MCP server directly
./scripts/dev setup                                 # Environment setup

# Examples:
./scripts/dev lint      # Quick style check during development
./scripts/dev format    # Format before committing
./scripts/dev run       # Test CLI changes quickly
```

#### When to Use Which Script

**Use `./scripts/test`** when:
- ✅ After making any code changes (your primary workflow)
- ✅ Before committing code
- ✅ Verifying everything works correctly
- ✅ Complete validation needed

**Use `./scripts/dev`** when:
- 🔧 Quick CLI testing during development
- 🔧 Formatting code (`./scripts/dev format`)
- 🔧 Just checking lint issues (`./scripts/dev lint`)
- 🔧 Starting MCP server for testing (`./scripts/dev server`)

### Manual Testing Commands

For granular testing when needed:

```bash
# Individual test components
uv run python -m pytest tests/ -v                   # Just pytest
uv run python -m flake8 src/ tests/ --max-line-length=100  # Just linting

# Specific test files
uv run python -m pytest tests/test_mock_data.py -v          # Core data tests
uv run python -m pytest tests/test_cli.py -v               # CLI tests
uv run python -m pytest tests/test_multi_agent.py -v       # Multi-agent tests

# Test with coverage
uv run python -m pytest tests/ --cov=src/payment_ops --cov-report=html

# Direct CLI testing
uv run payment-ops --help
uv run payment-ops -q "analyze"                    # Single agent
uv run payment-ops                                 # Interactive mode
```

#### Test Coverage

The test suite includes:
- **Data Layer Tests**: Mock database operations, payment retrieval, retry logic, escalation
- **CLI Tests**: Project structure validation, import verification
- **Multi-Agent Tests**: Agent class instantiation, MCP server verification, coordinator structure
- **Integration Tests**: End-to-end payment processing workflows and agent handoffs
- **Edge Cases**: Invalid payment IDs, error conditions, retry limits

**Test Files:**
- `test_mock_data.py`: Core payment database functionality (8 tests)
- `test_cli.py`: CLI structure and imports (2 tests)
- `test_multi_agent.py`: Multi-agent system components (9 tests)

**Total Test Coverage**: 19 tests covering single-agent, multi-agent, and integration scenarios

```bash
# View test results in detail
uv run python -m pytest tests/ -v --tb=short

# Run tests in parallel (faster)
uv run python -m pytest tests/ -n auto

# Run tests with output (for debugging)
uv run python -m pytest tests/ -v -s
```

### Troubleshooting

**Issue**: CLI shows import errors
```bash
# Use the correct entry point from project root
uv run payment-ops -q "analyze"

# Or use development script
./scripts/dev run -q "analyze"

# Don't run directly: python src/payment_ops/cli.py
```

**Issue**: Async cleanup warnings (rare)
If you see MCP client async warnings, they're harmless and don't affect functionality:
```bash
# Suppress stderr to hide warnings if needed
uv run payment-ops -q "analyze" 2>/dev/null

# The core payment processing always works correctly
```

**Issue**: OpenAI API errors
```bash
# Verify API key is set
cat .env | grep OPENAI_API_KEY

# Test API connectivity
python -c "import openai; print('API key configured')"
```

**Issue**: Import or path errors
```bash
# Run tests to verify structure
./scripts/test

# Check project structure
./scripts/dev help

# Reinstall package in development mode
uv pip install -e .
```


## Comprehensive Developer Testing Guide

Follow these steps to thoroughly test the entire codebase:

### 1. Initial Setup Verification
```bash
# Verify environment setup
cat .env | grep OPENAI_API_KEY  # Should show your API key
uv --version                    # Should show UV version
python --version                # Should show Python 3.11+
```

### 2. Run Complete Test Suite
```bash
# Run all tests (includes linting and syntax checks - now optimized!)
./scripts/test

# Expected result: 26 tests passing + clean linting
# - 8 tests: Mock data functionality
# - 2 tests: CLI structure and imports
# - 16 tests: Agent validation and multi-agent system components
# - Fast syntax check (only on main source files)
# - Complete in ~30 seconds (previously took much longer)
```

### 3. Test Single Agent Functionality
```bash
# Test single-query mode
uv run payment-ops -q "analyze"

# Expected: Should process 5 payments with summary:
# - 1 retry, 2 escalations, 2 no actions
# - Clean output with payment details
```

### 4. Test Multi-Agent Interactive Mode
```bash
# Start interactive CLI
uv run payment-ops

# Test each command:
> help                    # Should show all commands including multi-agent
> analyze                 # Single agent mode
> multi-agent            # Full 3-phase workflow
> compliance PAY-12345   # Compliance assessment for specific payment
> customer-service notify PAY-12345  # Customer service action
> history                # Should show all previous analyses
> exit
```

### 5. Verify Multi-Agent Workflow
```bash
uv run payment-ops
> multi-agent

# Expected output phases:
# Phase 1: Payment Operations (5 payments processed)
# Phase 2: Compliance Assessment (reviews for escalated payments)
# Phase 3: Customer Service (notifications sent)
# Summary: Handoffs completed, agents involved
```

### 6. Test Development Scripts
```bash
# Test development helper
./scripts/dev help       # Show available commands
./scripts/dev run        # Start CLI via dev script
./scripts/dev lint       # Quick lint check
./scripts/dev format     # Format code
./scripts/dev server     # Start MCP server directly

# Note: ./scripts/dev no longer has a 'test' command
# Use ./scripts/test directly for comprehensive validation
```

### 7. Verify Project Structure
```bash
# Check all agent files exist
ls src/payment_ops/agent/
# Should show: __init__.py, payment_ops.py, customer_service.py, compliance.py, multi_agent_coordinator.py

# Check all MCP servers exist
ls src/payment_ops/*/server.py
# Should show: payment_mcp/server.py, customer_mcp/server.py, compliance_mcp/server.py

# Check tests cover everything
ls tests/
# Should show: test_cli.py, test_mock_data.py, test_multi_agent.py
```

### 8. Test Error Handling
```bash
# Test with invalid API key (temporarily)
mv .env .env.backup
uv run payment-ops -q "analyze"
# Should show graceful error handling
mv .env.backup .env
```

### 9. Performance Testing
```bash
# Test startup time
time uv run payment-ops -q "analyze"
# Should complete in under 30 seconds

# Test multi-agent performance
time (uv run payment-ops <<< "multi-agent
exit")
# Should complete multi-agent workflow
```

### 10. Integration Testing
```bash
# Test that all agents can be imported
python -c "from src.payment_ops.agent.multi_agent_coordinator import MultiAgentCoordinator; print('✅ All imports work')"

# Test CLI entry point
uv run payment-ops --help
# Should show help without errors
```

**Success Criteria:**
- ✅ All 26 tests pass with clean linting
- ✅ Single agent processes 5 payments correctly
- ✅ Multi-agent workflow completes all 3 phases
- ✅ All CLI commands work without errors
- ✅ No import or path errors
- ✅ Fast performance (< 30 seconds for full test suite)
- ✅ Development scripts work for individual tasks

## Learning Resources

This codebase serves as a practical example of:
- **OpenAI Agents SDK**: Modern multi-agent development patterns
- **Model Context Protocol**: Standardized tool integration across multiple agents
- **Payment Operations**: Real-world business logic implementation with specialist agents
- **CLI Design**: Professional terminal application with multi-agent support
- **Agent Coordination**: Handoff patterns and workflow orchestration

**Educational Files**:
- `payments_ops_prd.md` - Complete project requirements and Phase 2 completion status
- `CONTINUATION_PROMPT.md` - Project continuation guide with Phase 3 options
- Agent code includes extensive comments explaining multi-agent design decisions

