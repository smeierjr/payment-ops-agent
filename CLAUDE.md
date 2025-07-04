# Payment Operations Agent - Claude Code Context

## Project Overview
Learning project for OpenAI Agent SDK mastery through realistic payment processing workflows.

**Current Status**: Refactoring to proper OpenAI SDK patterns  
**Reference**: See `OPENAI_AGENT_SDK_REFACTOR_PLAN.md` for complete implementation roadmap

## Quick Commands

```bash
# Primary development workflow
./scripts/test                           # Run tests (use before/after changes)
uv run payment-ops -q "analyze"          # Test CLI functionality
uv run payment-ops                       # Interactive mode

# Development helpers
./scripts/dev run -q "test query"        # Dev script testing
./scripts/dev test                       # Alternative test runner
```

## File Structure & Refactoring Targets

```
src/payment_ops/
├── cli.py                              # 🎯 REFACTOR: Simplify entry point
├── agent/
│   ├── payment_ops_orchestrator.py     # 🎯 MAIN TARGET: SDK handoffs
│   ├── payment_ops.py                  # Core agent (specialize)
│   ├── compliance_specialist.py        # Keep as-is
│   ├── customer_service_specialist.py  # Keep as-is
│   └── multi_agent_coordinator.py      # 🗑️ REMOVE: Custom orchestration
└── unified_mcp/server.py               # 🗑️ REPLACE: Monolithic → specialized
```

## Development Workflow for Claude Code

### Session Structure
1. **Context Loading**: Read refactor plan first, then specific implementation files
2. **Single Phase Focus**: Work on one refactor phase at a time  
3. **Frequent Validation**: Test after each significant change
4. **File Reading Priority**: Implementation targets > reference files > tests

### File Reading Strategy
**Essential for every session:**
- `OPENAI_AGENT_SDK_REFACTOR_PLAN.md` (roadmap)
- Target files based on current phase

**Read when implementing specific features:**
- Test files (only when writing/fixing tests)
- Mock data files (only when modifying business logic)
- Error handling (only when debugging)

**Avoid reading unless required:**
- Build artifacts (pyproject.toml, uv.lock)
- Legacy files marked for removal
- Documentation files beyond the refactor plan

## Environment & Setup

**Tech Stack**: Python 3.11+ + UV + OpenAI Agents SDK + MCP + FastMCP

**Quick Setup**:
```bash
uv sync                    # Install dependencies  
cp .env.example .env       # Add OPENAI_API_KEY
```

## Business Logic (Stable - Don't Change)

**Payment Processing Rules**:
- Insufficient funds → Escalate + notify customer
- Technical failure < 24hrs → Retry once  
- Compliance hold → Escalate to compliance
- Card declined (retry limit) → No action
- Unknown error → Escalate with context

**Test Data**: Always processes PAY-12345 through PAY-12349 with predictable outcomes

## Code Conventions

- **Imports**: Absolute from `src.payment_ops.*`
- **Async**: Proper cleanup with `await agent.cleanup()`  
- **Line Length**: 100 characters max
- **OpenAI SDK**: Follow documented patterns for agents/handoffs/tracing
- **Testing**: TDD approach during refactoring

## Expected Behaviors (Normal)

- MCP cleanup warnings during shutdown (harmless)
- "Processing 5 payments" message (uses mock data)
- Consistent business logic results across runs

## Common Errors & Solutions

**Import Errors**: Use `uv run payment-ops` not `python src/...`  
**Module Not Found**: Run `uv sync` to fix virtual environment  
**Test Failures**: Check import paths after refactoring

## Success Criteria

**Functional**: All CLI workflows work with new SDK patterns  
**Learning**: Deep hands-on experience with Agent SDK capabilities  
**Quality**: >90% test coverage, proper tracing, clean architecture

---

*Use OPENAI_AGENT_SDK_REFACTOR_PLAN.md as the primary implementation guide. This file provides Claude Code context and efficient development workflows.*