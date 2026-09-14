import json
import re
import subprocess
from datetime import datetime
import sys

from ai.failure_analyzer import FailureAnalyzer


class TestRunner:

    def __init__(self):

        self.failure_analyzer = FailureAnalyzer()
        # self.failure_analyzer = None

    def run_test(self, test_file: str):

        result = subprocess.run(
            [
                "pytest",
                test_file,
                "-v"
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL
        )


        print("\n===== PYTEST OUTPUT =====\n", file=sys.stderr)
        print(result.stdout, file=sys.stderr)

        if result.stderr:
            print("\n===== PYTEST ERRORS =====\n", file=sys.stderr)
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:

            print("\n===== TEST RESULT =====")
            print("PASS")

            return

        print("\n===== TEST RESULT =====")
        print("FAIL")

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
            output += "\n\n===== PYTEST ERRORS =====\n"
            output += result.stderr

        if result.returncode == 0:
            status = "ALL TESTS PASSED"
        else:
            status = "ONE OR MORE TESTS FAILED"

        test_results = []

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

            test_path = line.split(
                " ",
                1
            )[0]

            if "::" not in test_path:
                continue

            test_file = test_path.split(
                "::",
                1
            )[0]

            test_name = test_path.split(
                "::",
                1
            )[1]

            test_name = re.sub(
                r"\[.*\]$",
                "",
                test_name
            )

            test_id = self.extract_test_case_id(
                test_file
            )

            if "PASSED" in line:
                test_status = "PASSED"
            else:
                test_status = "FAILED"

            test_results.append(
                {
                    "test_case_id": test_id,
                    "test_name": test_name,
                    "test_file": test_file,
                    "status": test_status
                }
            )

        failed_tests = [
            test
            for test in test_results
            if test["status"] == "FAILED"
        ]

        for failed_test in failed_tests:

            test_file = failed_test["test_file"]
            test_name = failed_test["test_name"]

            error_output = self.extract_failure_output(
                result.stdout,
                test_name
            )

            if self.failure_analyzer:
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

                failed_test["ai_analysis"] = analysis

        # for failed_test in failed_tests:
        #     test_file = failed_test["test_file"]
        #     test_name = failed_test["test_name"]
        #
        #     error_output = self.extract_failure_output(
        #         result.stdout,
        #         test_name
        #     )
        #
        #     with open(
        #             test_file,
        #             "r",
        #             encoding="utf-8"
        #     ) as file:
        #         test_code = file.read()
        #
        #     analysis = self.failure_analyzer.analyze(
        #         test_name=test_name,
        #         error_message=error_output,
        #         test_code=test_code
        #     )
        #
        #     failed_test["ai_analysis"] = analysis

        report = {

            "execution_time": datetime.now().isoformat(),

            "summary": {

                "total": len(test_results),

                "passed": len(
                    [
                        test
                        for test in test_results
                        if test["status"] == "PASSED"
                    ]
                ),

                "failed": len(
                    [
                        test
                        for test in test_results
                        if test["status"] == "FAILED"
                    ]
                )
            },

            "tests": test_results
        }

        self.save_report(report)

        return {
            "status": status,
            "exit_code": result.returncode,
            "pytest_output": output,
            "tests": test_results,
            "report": report
        }

    # def run_all_generated_tests(self):
    #
    #     result = subprocess.run(
    #         [
    #             "pytest",
    #             "tests/generated",
    #             "-v"
    #         ],
    #         capture_output=True,
    #         text=True,
    #         stdin=subprocess.DEVNULL
    #     )
    #
    #     # result = subprocess.run(
    #     #     [
    #     #         "pytest",
    #     #         "tests/generated",
    #     #         "-v"
    #     #     ],
    #     #     capture_output=True,
    #     #     text=True
    #     # )
    #
    #     print("\n===== PYTEST OUTPUT =====\n")
    #     print(result.stdout)
    #
    #     if result.stderr:
    #
    #         print("\n===== PYTEST ERRORS =====\n")
    #         print(result.stderr)
    #
    #     test_results = []
    #
    #     for line in result.stdout.splitlines():
    #
    #         line = line.strip()
    #
    #         if "::" not in line:
    #             continue
    #
    #         if (
    #             " PASSED " not in line
    #             and not line.endswith(" PASSED")
    #             and " FAILED " not in line
    #             and not line.endswith(" FAILED")
    #         ):
    #             continue
    #
    #         test_path = line.split(
    #             " ",
    #             1
    #         )[0]
    #
    #         if "::" not in test_path:
    #             continue
    #
    #         test_file = test_path.split(
    #             "::",
    #             1
    #         )[0]
    #
    #         test_name = test_path.split(
    #             "::",
    #             1
    #         )[1]
    #
    #         test_name = re.sub(
    #             r"\[.*\]$",
    #             "",
    #             test_name
    #         )
    #
    #         test_id = self.extract_test_case_id(
    #             test_file
    #         )
    #
    #         if "PASSED" in line:
    #
    #             status = "PASSED"
    #
    #         else:
    #
    #             status = "FAILED"
    #
    #         test_results.append(
    #             {
    #                 "test_case_id": test_id,
    #                 "test_name": test_name,
    #                 "test_file": test_file,
    #                 "status": status
    #             }
    #         )
    #
    #     if result.returncode == 0:
    #
    #         print("\n===== TEST RESULT =====")
    #         print("ALL TESTS PASSED")
    #
    #     else:
    #
    #         print("\n===== TEST RESULT =====")
    #         print("ONE OR MORE TESTS FAILED")
    #
    #     print("\n===== TEST CASE RESULTS =====")
    #
    #     for test in test_results:
    #
    #         print(
    #             f"{test['test_case_id']} | "
    #             f"{test['test_name']} | "
    #             f"{test['status']}"
    #         )
    #
    #     failed_tests = [
    #         test
    #         for test in test_results
    #         if test["status"] == "FAILED"
    #     ]
    #
    #     for failed_test in failed_tests:
    #
    #         test_file = failed_test["test_file"]
    #
    #         test_name = failed_test["test_name"]
    #
    #         print(
    #             f"\n===== ANALYZING "
    #             f"{failed_test['test_case_id']} ====="
    #         )
    #
    #         error_output = (
    #             self.extract_failure_output(
    #                 result.stdout,
    #                 test_name
    #             )
    #         )
    #
    #         with open(
    #             test_file,
    #             "r",
    #             encoding="utf-8"
    #         ) as file:
    #
    #             test_code = file.read()
    #
    #         print(
    #             "\n===== EXTRACTED FAILURE =====\n"
    #         )
    #
    #         print(error_output)
    #
    #         analysis = self.failure_analyzer.analyze(
    #             test_name=test_name,
    #             error_message=error_output,
    #             test_code=test_code
    #         )
    #
    #         failed_test["ai_analysis"] = analysis
    #
    #         print(
    #             "\n===== AI FAILURE ANALYSIS =====\n"
    #         )
    #
    #         print(analysis)
    #
    #     report = {
    #
    #         "execution_time": datetime.now().isoformat(),
    #
    #         "summary": {
    #
    #             "total": len(test_results),
    #
    #             "passed": len(
    #                 [
    #                     test
    #                     for test in test_results
    #                     if test["status"] == "PASSED"
    #                 ]
    #             ),
    #
    #             "failed": len(
    #                 [
    #                     test
    #                     for test in test_results
    #                     if test["status"] == "FAILED"
    #                 ]
    #             )
    #         },
    #
    #         "tests": test_results
    #     }
    #
    #     self.save_report(report)
    #
    #     return test_results

    def extract_test_case_id(
        self,
        test_file: str
    ) -> str:

        filename = test_file.split("/")[-1]

        filename = filename.split("\\")[-1]

        match = re.search(
            r"(TC-[A-Za-z0-9-]+)",
            filename
        )

        if match:

            return match.group(1)

        return "UNKNOWN"

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

                failure_lines.append(
                    line
                )

            if (
                collecting
                and line.startswith("FAILED ")
            ):

                break

        if failure_lines:

            return "\n".join(
                failure_lines
            )

        return pytest_output

    def save_report(
        self,
        report: dict
    ):

        report_file = (
            "reports/"
            "test_execution_report.json"
        )

        with open(
            report_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(
            "\n===== REPORT ====="
        )

        print(
            f"Report saved to: "
            f"{report_file}"
        )
