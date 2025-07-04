#!/usr/bin/env python3
"""
Simple Payment Operations CLI - No complex dependencies
Works with any terminal including Ghostty
"""

import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / ".env")


def print_banner():
    """Print simple banner"""
    print("=" * 80)
    print("🤖 Payment Operations CLI - Orchestrator System")
    print("=" * 80)
    print("Commands: help, history, exit. Any other input is sent to the orchestrator.")
    print()


def print_help():
    """Print help information"""
    print("\n📋 Available Commands:")
    print("  <any text>         - Send a query to the Payment Operations Orchestrator")
    print("  help               - Show this help")
    print("  history            - Show previous analysis results")
    print("  exit               - Exit CLI")
    print("\nExamples:")
    print("  > analyze pending payments")
    print("  > process high-risk payment PAY-12347")
    print()


async def run_orchestrator_workflow(
    query="Process all pending payments systematically", history_list=None
):
    """Ultra-simple launcher for self-contained orchestrator"""
    try:
        from datetime import datetime
        from src.payment_ops.agent.payment_ops_orchestrator import (
            PaymentOpsOrchestrator,
        )

        print("🚀 Starting Payment Operations Orchestrator...")
        print("   🎯 Self-contained payment processing workflow")
        print("   🔄 Smart Handoffs: Compliance & Customer Service as needed")
        print("   🔍 SDK Tracing: Enabled for complete observability")

        # Use async context manager for clean lifecycle management
        async with PaymentOpsOrchestrator() as orchestrator:
            result = await orchestrator.run(query)
            handoffs_triggered = result.get("orchestration_summary", {}).get(
                "handoffs_triggered", 0
            )
            print(f"✅ [CLI] Execution completed with {handoffs_triggered} handoffs")

            # Format orchestrator output
            if result["status"] == "error":
                error_msg = f"❌ Orchestrator Error: {result.get('error', 'Unknown error')}"
                print(error_msg)
                # Note: SDK handles error recording automatically
                # Error already captured in SDK trace
                return error_msg

            # Format orchestrator results with tracing information
            output = "🚀 Payment Operations Orchestrator Summary\n"
            output += "=" * 90 + "\n"

            # SDK Tracing Summary
            sdk_tracing = result.get("sdk_tracing", {})
            if sdk_tracing.get("tracing_enabled"):
                output += "\n🔍 SDK Tracing Information\n"
                output += "-" * 50 + "\n"
                output += f"Workflow Trace ID: {sdk_tracing.get('workflow_trace_id', 'N/A')}\n"
                output += f"Workflow Name: {sdk_tracing.get('workflow_name', 'N/A')}\n"
                tracing_status = '✅ Active' if sdk_tracing.get('tracing_enabled') else '❌ Disabled'
                output += f"Tracing Status: {tracing_status}\n"

            # Orchestration Summary
            orchestration = result.get("orchestration_summary", {})
            output += "\n🎯 Orchestration Details\n"
            output += "-" * 50 + "\n"
            primary_agent = orchestration.get('primary_agent', 'PaymentOpsOrchestrator')
            output += f"Primary Agent: {primary_agent}\n"
            output += f"Handoffs Triggered: {orchestration.get('handoffs_triggered', 0)}\n"
            agents_involved = orchestration.get("agents_involved", [])
            output += f"Agents Involved: {', '.join(agents_involved)}\n"

            # Decision Points
            decision_points = orchestration.get("decision_points", [])
            if decision_points:
                output += "\n🧠 Decision Points:\n"
                for i, point in enumerate(decision_points, 1):
                    output += f"  {i}. {point}\n"

            # Final Response
            final_response = result.get("final_response", "")
            if final_response:
                output += """

📋 Orchestrator Response:
"""
                output += "-" * 50 + "\n"
                # Show full response for comprehensive analysis
                display_response = final_response
                output += display_response + "\n"

            output += "\n" + "=" * 90
            print(output)

            # Store in history with tracing information
            if history_list is not None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_entry = {
                    "timestamp": timestamp,
                    "query": f"orchestrator: {query}",
                    "output": output,
                    "trace_ids": {
                        "workflow_trace_id": sdk_tracing.get("workflow_trace_id"),
                    },
                }
                history_list.append(history_entry)
                if len(history_list) > 10:
                    history_list.pop(0)

            return output

    except Exception as e:
        error_msg = f"❌ Orchestrator Error: {e}"
        print(error_msg)
        return error_msg


def show_analysis_history(history_list):
    """Show previous payment analysis results"""
    if not history_list:
        print("\n📋 No previous analyses found")
        print("Run 'analyze' to perform your first payment analysis")
        return

    print(f"\n📋 Payment Analysis History ({len(history_list)} results)")
    print("=" * 60)

    for i, entry in enumerate(history_list, 1):
        timestamp = entry["timestamp"]
        query = entry["query"][:40] + "..." if len(entry["query"]) > 40 else entry["query"]
        print(f"{i:2}. {timestamp} | {query}")

    print("=" * 60)

    try:
        choice = input("\nEnter number to view details (or press Enter to continue): ").strip()

        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(history_list):
                entry = history_list[idx]
                print(f"\n🕐 Analysis from {entry['timestamp']}")
                print(f"📝 Query: {entry['query']}")
                print("-" * 60)
                print(entry["output"])
                print("-" * 60)
            else:
                print("❌ Invalid number")

    except KeyboardInterrupt:
        print("\n💭 Input cancelled (Ctrl+C)")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main CLI loop"""
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python payment-ops.py [--help]")
            print("       python payment-ops.py")
            print("       python payment-ops.py -q 'query'")
            return
        elif sys.argv[1] == "-q" and len(sys.argv) > 2:
            # Single query mode
            query = " ".join(sys.argv[2:])
            asyncio.run(run_orchestrator_workflow(query))
            return

    # Interactive mode
    print_banner()

    analysis_history = []

    while True:
        try:
            # Simple input prompt
            user_input = input("payment-ops> ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye!")
                break

            elif user_input.lower() in ["help", "?"]:
                print_help()

            elif user_input.lower() == "history":
                show_analysis_history(analysis_history)

            elif user_input.lower() in ["clear", "cls"]:
                clear_cmd = "clear" if os.name == "posix" else "cls"
                os.system(clear_cmd)
                print_banner()

            else:
                # Any other input is treated as a query for the orchestrator
                asyncio.run(run_orchestrator_workflow(user_input, analysis_history))

        except KeyboardInterrupt:
            print("\n💭 Input cancelled (Ctrl+C)")
            continue
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def cli_main():
    """Entry point for the CLI"""
    main()


if __name__ == "__main__":
    cli_main()
