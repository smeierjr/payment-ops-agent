# Payment Operations Agent - Learning Project

A learning project for mastering OpenAI's Agent SDK through realistic payment processing workflows. Features multi-agent coordination with specialist agents for compliance and customer service.

## Overview

This project demonstrates modern multi-agent AI architecture through a practical payment operations use case. The system coordinates between a primary orchestrator and specialized agents (Customer Service and Compliance) to handle failed payments with comprehensive workflow automation.

**Key Features:**
- **Multi-Agent Architecture**: Coordinated specialist agents with handoff patterns
- **MCP Protocol**: Unified tool integration across all agents
- **Learning-Focused CLI**: Clean terminal interface for educational exploration
- **Cost Optimized**: Uses GPT-4o-mini for ~85% cost savings
- **Business Logic**: Real payment operations, compliance, and customer service workflows
- **Full Traceability**: Complete audit trail of all actions and agent handoffs

## Architecture

```
┌─────────────────┐                    ┌─────────────────────────┐
│   CLI Interface │ ──────────────────►│ Payment Ops Orchestrator│
│   (Simple CLI)  │                    │   (Primary Agent)       │
└─────────────────┘                    └─────────┬───────────────┘
                                                 │
                          ┌──────────────────────┼──────────────────────┐
                          ▼                      ▼                      ▼
               ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
               │ Payment Ops     │    │ Customer Service│    │ Compliance      │
               │ Orchestrator    │    │ Specialist      │    │ Specialist      │
               └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
                         │                      │                      │
                         └──────────────────────┼──────────────────────┘
                                                ▼
                                    ┌─────────────────────────┐
                                    │   Unified MCP Server    │
                                    │  (7 Payment Tools)      │
                                    └─────────────────────────┘
```

**Technology Stack:**
- **Agent Framework**: OpenAI Agents SDK with multi-agent coordination
- **Tool Protocol**: Model Context Protocol (MCP) with unified server
- **CLI Framework**: Pure Python with educational focus
- **Package Manager**: UV for fast, reliable dependency management
- **Model**: GPT-4o-mini for cost-effective operations
- **Architecture**: Specialist agents with handoff patterns

## Quick Start

### Prerequisites

- Python 3.11+
- [UV package manager](https://docs.astral.sh/uv/)
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/smeierjr/payment-ops-agent.git
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
uv run payment-ops -q "analyze pending payments"  # Single query
uv run payment-ops  # Interactive mode

# 2. Using development scripts
./scripts/dev run -q "analyze pending payments"
./scripts/dev run  # Interactive mode

# Show help
uv run payment-ops --help

# ❌ Don't run directly (causes import errors):
# python src/payment_ops/cli.py
```

## CLI Interface

The CLI provides both single-shot and interactive modes designed for learning and experimentation.

### Interactive Mode

```bash
$ uv run payment-ops
================================================================================
🤖 Payment Operations CLI - Learning Project
================================================================================
Commands: help, history, exit, or enter any payment analysis query

payment-ops> analyze pending payments
🚀 Payment Operations Analysis
Processing 5 payments through multi-agent coordination...

📊 Payment Processing Results
==========================================================================================
1. PAY-12345 ($1,500.00): INSUFFICIENT_FUNDS → Escalate + notify customer
2. PAY-12346 ($2,500.00): TECHNICAL_FAILURE → Retry (< 24hrs old)
3. PAY-12347 ($7,500.00): COMPLIANCE_HOLD → Escalate to compliance
4. PAY-12348 ($800.00): CARD_DECLINED → Customer action required
5. PAY-12349 ($1,200.00): UNKNOWN_ERROR → Escalate with context

📈 Summary: 1 retry, 3 escalations, 1 customer action
==========================================================================================

payment-ops> history
📋 Previous Analysis Results
1. [2025-01-15 10:30:00] analyze pending payments (trace: pay-ops-20250115-103000)
2. [2025-01-15 10:25:00] what payments need attention (trace: pay-ops-20250115-102500)

payment-ops> exit
👋 Goodbye!
```

### Available Commands

- **Any text query** - Sent to Payment Operations Orchestrator
- **`help`** - Show available commands
- **`history`** - View previous analysis results with trace IDs
- **`exit`** - Exit the CLI

### Single Query Mode

For automation and scripting:

```bash
# Single query analysis
uv run payment-ops -q "analyze pending payments"

# Custom analysis queries
uv run payment-ops -q "what payments need attention?"
uv run payment-ops -q "retry failed technical payments"
```

## Business Logic

The multi-agent system implements realistic payment operations workflows:

### Payment Operations Orchestrator
- **Insufficient Funds** → Escalate with customer notification
- **Technical Failure** → Retry once if < 24 hours old, else escalate
- **Compliance Hold** → Escalate to compliance team
- **Card Declined** → Customer action required
- **Unknown Errors** → Escalate with full context

### Compliance Specialist
- **AML Compliance Checks** → Risk scoring and assessment
- **Risk Assessment** → LOW/MEDIUM/HIGH risk classification
- **Regulatory Review** → Manual review for high-risk transactions
- **International Transactions** → Enhanced due diligence

### Customer Service Specialist
- **Customer Notifications** → Automated communication about payment issues
- **Service Tiers** → VIP/Business/Standard customer handling
- **Communication Preferences** → Email/phone preference management
- **Follow-up Scheduling** → Automated customer outreach planning

### Agent Coordination
- **Individual Payment Processing** → Each payment analyzed separately for educational clarity
- **Handoff Logic** → Business rules determine when to involve specialists
- **Trace Tracking** → Each payment gets unique workflow trace for observability

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
│   └── payment_ops/                    # Main package
│       ├── __init__.py
│       ├── cli.py                      # Simple CLI interface
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── payment_ops_orchestrator.py  # Main orchestrator
│       │   ├── customer_service_specialist.py # Customer service agent
│       │   └── compliance_specialist.py      # Compliance agent
│       ├── unified_mcp/                # Single MCP server
│       │   ├── __init__.py
│       │   └── server.py               # 7 payment tools
│       ├── data/
│       │   ├── __init__.py
│       │   └── mock_payments.py        # Test payment data
│       └── errors.py                   # Error handling
├── tests/                              # Test suite
│   ├── test_mock_data.py
│   ├── test_cli.py
│   ├── test_multi_agent.py
│   └── test_agent_validation.py
├── scripts/                            # Development scripts
│   ├── dev                             # Development helper
│   └── test                            # Test runner
└── pyproject.toml                      # Project configuration
```

### Key Components

**Payment Operations Orchestrator** (`src/payment_ops/agent/payment_ops_orchestrator.py`):
- Main agent coordinating payment processing workflows
- Implements handoff logic to specialist agents
- Uses OpenAI Agent SDK patterns for proper agent coordination
- Processes individual payments with clear business logic

**Customer Service Specialist** (`src/payment_ops/agent/customer_service_specialist.py`):
- Handles customer communications and notifications
- Manages VIP/Business/Standard customer tiers
- Implements service level agreements per customer type

**Compliance Specialist** (`src/payment_ops/agent/compliance_specialist.py`):
- Conducts risk assessment and compliance checks
- Handles AML compliance and regulatory requirements
- Manages HIGH/MEDIUM/LOW risk classifications

**Unified MCP Server** (`src/payment_ops/unified_mcp/server.py`):
- Single MCP server providing 7 payment tools
- Tools: get_pending_payments, get_payment_details, retry_payment, escalate_payment, assess_payment_risk, notify_customer, get_action_log
- Shared across all agents for consistent tool access

**Simple CLI Interface** (`src/payment_ops/cli.py`):
- Interactive and single-query modes
- History tracking with trace IDs
- Clean terminal interface with no complex dependencies

### Development Scripts

The project provides two optimized scripts for different development workflows:

#### `./scripts/test` - Primary Validation Script
**Use this after making code changes** - your main quality gate:

```bash
# Run complete validation suite (fast & comprehensive)
./scripts/test

# Includes:
# ✅ All pytest tests 
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
./scripts/dev lint                                  # Just linting
./scripts/dev format                                # Auto-format code with black
./scripts/dev server                                # Start MCP server directly
./scripts/dev setup                                 # Environment setup
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
uv run python -m pytest tests/test_agent_validation.py -v  # Agent validation tests

# Direct CLI testing
uv run payment-ops --help
uv run payment-ops -q "analyze"                    # Single query
uv run payment-ops                                 # Interactive mode
```

#### Test Coverage

Current test suite covers:
- **Data Layer**: Mock database operations, payment processing logic
- **CLI Structure**: Import validation and basic CLI functionality  
- **Agent System**: Agent instantiation and coordination
- **Multi-Agent Workflows**: Individual payment processing patterns

**Test Files:**
- `test_mock_data.py`: Core payment database functionality
- `test_cli.py`: CLI structure and imports validation
- `test_multi_agent.py`: Agent system components
- `test_agent_validation.py`: Agent validation and coordination

**Run Tests:**
```bash
./scripts/test                          # Complete validation suite
uv run python -m pytest tests/ -v      # Individual test execution
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

## Learning Project Goals

This codebase serves as a hands-on learning project for:
- **OpenAI Agent SDK**: Modern multi-agent development patterns
- **Agent Handoffs**: Proper coordination between specialist agents
- **MCP Integration**: Tool sharing across multiple agents
- **Payment Processing**: Realistic business logic implementation
- **CLI Design**: Professional terminal application development

**Current Learning Phase**: Refactoring to proper OpenAI SDK patterns
**Reference**: See `OPENAI_AGENT_SDK_REFACTOR_PLAN.md` for implementation roadmap

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
# Run all tests (includes linting and syntax checks)
./scripts/test

# Expected result: All tests passing + clean linting
```

### 3. Test CLI Functionality
```bash
# Test single-query mode
uv run payment-ops -q "analyze pending payments"

# Expected: Should process 5 payments with summary
```

### 4. Test Interactive Mode
```bash
# Start interactive CLI
uv run payment-ops

# Test commands:
> help                    # Show available commands
> analyze                 # Payment analysis
> history                 # Previous analyses
> exit
```

### 5. Test Development Scripts
```bash
# Test development helper
./scripts/dev help       # Show available commands
./scripts/dev run        # Start CLI via dev script
./scripts/dev lint       # Quick lint check
./scripts/dev format     # Format code
```

**Success Criteria:**
- ✅ All tests pass with clean linting
- ✅ CLI processes 5 payments correctly
- ✅ Interactive mode works without errors
- ✅ No import or path errors
- ✅ Fast performance (< 30 seconds for full test suite)
- ✅ Development scripts work for individual tasks

## Learning Resources

**Educational Files**:
- `OPENAI_AGENT_SDK_REFACTOR_PLAN.md` - Complete implementation roadmap
- `CLAUDE.md` - Project context and development workflow
- Agent code includes extensive comments explaining multi-agent design decisions

This project provides practical experience with modern AI agent development patterns while implementing realistic business workflows.