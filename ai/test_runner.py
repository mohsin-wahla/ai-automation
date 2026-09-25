import json
import re
import subprocess
from ai.safe_healer import SafeHealer

from datetime import datetime
from pathlib import Path

from ai.failure_analyzer import FailureAnalyzer
from ai.html_reporter import HTMLReporter


class TestRunner:

    def __init__(self):
        self.failure_analyzer = FailureAnalyzer()
        self.safe_healer = SafeHealer()
        self.html_reporter = HTMLReporter()

    def run_all_generated_tests(self):

        result = subprocess.run(
            [
                "pytest",
                "tests/generated",
                "-v"
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL
        )

        output = result.stdout

        if result.stderr:
            output += (
                "\n\n===== PYTEST ERRORS =====\n"
                + result.stderr
            )

        initial_status = (
            "ALL TESTS PASSED"
            if result.returncode == 0
            else "ONE OR MORE TESTS FAILED"
        )

        test_results = []

        # --------------------------------
        # Parse pytest results
        # --------------------------------

        for line in result.stdout.splitlines():

            line = line.strip()

            if "::" not in line:
                continue

            if (
                " PASSED " not in line
                and not line.endswith(" PASSED")
                and " FAILED " not in line
                and not line.endswith(" FAILED")
            ):
                continue

            test_path = line.split(" ", 1)[0]

            if "::" not in test_path:
                continue

            test_file, test_name = test_path.split(
                "::",
                1
            )

            test_name = re.sub(
                r"\[.*\]$",
                "",
                test_name
            )

            if "PASSED" in line:
                test_status = "PASSED"
            else:
                test_status = "FAILED"

            test_results.append(
                {
                    "test_case_id": self.extract_test_case_id(
                        test_file
                    ),
                    "test_name": test_name,
                    "test_file": test_file,
                    "status": test_status
                }
            )

        # --------------------------------
        # Failure analysis
        # --------------------------------

        failed_tests = [
            test
            for test in test_results
            if test["status"] == "FAILED"
        ]

        if self.failure_analyzer:

            for failed_test in failed_tests:

                test_file = failed_test["test_file"]
                test_name = failed_test["test_name"]

                error_output = self.extract_failure_output(
                    result.stdout,
                    test_name
                )

                try:

                    with open(
                        test_file,
                        "r",
                        encoding="utf-8"
                    ) as file:
                        test_code = file.read()

                    analysis = self.failure_analyzer.analyze(
                        test_name=test_name,
                        error_message=error_output,
                        test_code=test_code
                    )

                    failed_test["ai_analysis"] = analysis.model_dump()

                    healing_result = self.safe_healer.heal(
                        test_file=test_file,
                        analysis=analysis,
                        failure_output=error_output,
                    )

                    failed_test["self_healing"] = healing_result
                    if healing_result["healing_applied"]:

                        rerun_result = self._rerun_test(test_file)

                        failed_test["self_healing"]["rerun"] = rerun_result

                        if rerun_result["passed"]:
                            failed_test["status"] = "HEALED"
                        else:
                            failed_test["status"] = "FAILED_AFTER_HEALING"


                except Exception as error:

                    failed_test["self_healing"] = {

                        "healing_attempted": False,

                        "healing_applied": False,

                        "healing_type": "none",

                        "changed_file": None,

                        "original_code": None,

                        "updated_code": None,

                        "reason": (

                            f"Self-healing process failed: {error}"

                        ),

                    }

        # --------------------------------
        # Final report
        # --------------------------------

        passed_count = sum(
            1
            for test in test_results
            if test["status"] == "PASSED"
        )

        failed_count = sum(
            1
            for test in test_results
            if test["status"] == "FAILED"
        )

        healed_count = sum(
            1
            for test in test_results
            if test.get("self_healing", {}).get(
                "healing_applied",
                False
            )
        )
        final_failed_count = sum(
            1
            for test in test_results
            if test["status"] in (
                "FAILED",
                "FAILED_AFTER_HEALING"
            )
        )

        final_status = (
            "ALL TESTS PASSED"
            if final_failed_count == 0
            else "ONE OR MORE TESTS FAILED"
        )

        report = {

            "execution_time": datetime.now().isoformat(),

            "summary": {
                "total": len(test_results),
                "passed": passed_count,
                "failed": failed_count,
                "healed": healed_count
            },

            "tests": test_results,

            "final_status": final_status
        }

        self.save_report(report)

        return {
            "status": final_status,
            "exit_code": result.returncode,
            "pytest_output": output,
            "tests": test_results,
            "report": report
        }

    # --------------------------------
    # Extract test case ID from filename
    # --------------------------------

    def extract_test_case_id(
        self,
        test_file: str
    ) -> str:

        filename = Path(test_file).name

        match = re.search(
            r"(TC[-_][A-Za-z0-9_-]+)",
            filename
        )

        if match:
            return match.group(1)

        return "UNKNOWN"

    # --------------------------------
    # Extract failure information
    # --------------------------------

    def extract_failure_output(
        self,
        pytest_output: str,
        test_name: str
    ) -> str:

        lines = pytest_output.splitlines()

        collecting = False
        failure_lines = []

        for line in lines:

            if (
                line.startswith("_")
                and test_name in line
            ):
                collecting = True

            if collecting:
                failure_lines.append(line)

            if (
                collecting
                and line.startswith("FAILED ")
            ):
                break

        if failure_lines:
            return "\n".join(failure_lines)

        return pytest_output

    # --------------------------------
    # Rerun failed test after healing
    # --------------------------------
    def _rerun_test(self, test_file: str) -> dict:

        import subprocess
        import sys

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    test_file,
                    "-v",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            output = result.stdout + "\n" + result.stderr

            passed = result.returncode == 0

            return {
                "attempted": True,
                "passed": passed,
                "timed_out": False,
                "return_code": result.returncode,
                "output": output,
            }

        except subprocess.TimeoutExpired as error:

            stdout = error.stdout or ""
            stderr = error.stderr or ""

            return {
                "attempted": True,
                "passed": False,
                "timed_out": True,
                "return_code": None,
                "output": (
                        stdout
                        + "\n"
                        + stderr
                        + "\n\n"
                          "RERUN TIMEOUT: "
                          "targeted pytest exceeded 60 seconds."
                ),
            }
    def save_report(
            self,
            report: dict
    ):

        report_dir = (
                Path(__file__).resolve().parent.parent
                / "reports"
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------
        # Save JSON report
        # --------------------------------

        json_report_file = (
                report_dir
                / "test_execution_report.json"
        )

        with open(
                json_report_file,
                "w",
                encoding="utf-8"
        ) as file:
            json.dump(
                report,
                file,
                indent=4
            )

        print("\n===== REPORT =====")

        print(
            f"JSON report saved to: "
            f"{json_report_file}"
        )

        # --------------------------------
        # Generate HTML report
        # --------------------------------

        html_report_file = (
            self.html_reporter.generate(
                report
            )
        )

        print(
            f"HTML report saved to: "
            f"{html_report_file}"
        )

