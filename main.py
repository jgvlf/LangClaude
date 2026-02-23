import asyncio
from src.workflow import run_due_diligence


async def main():
    """Run the due diligence workflow."""
    print("Starting Due Diligence Workflow...\n")

    result = await run_due_diligence(
        startup_name="TechStartup Inc",
        startup_description="An AI-powered platform for automated testing"
    )

    print("\n--- Final State ---")
    print(f"Status: {result.get('current_stage')}")
    print(f"Errors: {result.get('errors', [])}")


if __name__ == "__main__":
    asyncio.run(main())