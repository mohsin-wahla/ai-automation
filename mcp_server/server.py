import json
from pathlib import Path
import os


from mcp.server.fastmcp import FastMCP

from ai.test_runner import TestRunner

print(
    "[SERVER] GEMINI_API_KEY:",
    bool(os.getenv("GEMINI_API_KEY"))
)


mcp = FastMCP("AI Automation Server")


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@mcp.tool()
def run_tests() -> str:
    """
    Run all generated Playwright tests through TestRunner.
    """


    runner = TestRunner()

    results = runner.run_all_generated_tests()

    return json.dumps(
        results,
        indent=4
    )

@mcp.tool()
def read_test_report() -> str:
    """
    Read the latest test execution report.
    """

    report_file = (
        PROJECT_ROOT
        / "reports"
        / "test_execution_report.json"
    )

    if not report_file.exists():
        return "Test execution report not found."

    return report_file.read_text(
        encoding="utf-8"
    )


if __name__ == "__main__":
    mcp.run()
