import asyncio
import json
import sys
from pathlib import Path
import os
import re

from ai.test_generator import TestCaseGenerator
from ai.automation_generator import AutomationGenerator

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class AutomationAgent:



    def __init__(self):

        self.project_root = (
            Path(__file__).resolve().parent.parent
        )

        self.test_generator = TestCaseGenerator()
        self.automation_generator = AutomationGenerator()

    def extract_user_story_id(self, user_story: str) -> str:
        """
        Extract user story ID such as:
        US001
        US002
        US-001
        US_001
        """

        match = re.search(
            r"\bUS[-_]?\d+\b",
            user_story,
            re.IGNORECASE
        )

        if not match:
            raise ValueError(
                "User story ID not found in user story."
            )

        return match.group(0).upper()

    def prepare_story_generated_folder(
            self,
            user_story_id: str
    ):
        """
        Remove only the generated automation
        belonging to the current user story.
        """

        generated_dir = (
                self.project_root
                / "tests"
                / "generated"
                / user_story_id
        )

        if generated_dir.exists():

            print(
                f"\n===== CLEANING {user_story_id} TESTS ====="
            )

            for test_file in generated_dir.glob(
                    "test_*.py"
            ):
                test_file.unlink()

                print(
                    f"Deleted: {test_file.name}"
                )

        else:

            generated_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            print(
                f"\nCreated generated folder: "
                f"{generated_dir}"
            )

        return generated_dir

    def read_user_story(self):

        user_story_path = (
            self.project_root
            / "test_data"
            / "user_story_cart.txt"
        )

        return user_story_path.read_text(
            encoding="utf-8"
        )

    def generate_test_cases(self, user_story):

        print("\n===== STEP 1: GENERATING TEST CASES =====")

        result = self.test_generator.generate(
            user_story
        )

        generated_path = (
            self.project_root
            / "test_data"
            / "generated_test_cases.json"
        )

        generated_path.write_text(
            json.dumps(
                result.model_dump(),
                indent=2
            ),
            encoding="utf-8"
        )

        print(
            f"Generated {len(result.test_cases)} test cases."
        )

        return result

    def approve_test_cases(self, test_cases):

        print("\n===== STEP 2: APPROVING TEST CASES =====")

        approved_path = (
            self.project_root
            / "test_data"
            / "approved_test_cases.json"
        )

        approved_path.write_text(
            json.dumps(
                test_cases.model_dump(),
                indent=2
            ),
            encoding="utf-8"
        )

        candidates = [
            test_case
            for test_case in test_cases.test_cases
            if test_case.automation_candidate
        ]

        print(
            f"Approved {len(test_cases.test_cases)} test cases."
        )

        print(
            f"Automation candidates: {len(candidates)}"
        )

        return candidates

    def generate_automation(
            self,
            candidates,
            user_story_id
    ):

        print(
            "\n===== STEP 3: GENERATING AUTOMATION ====="
        )

        generated_files = []

        for test_case in candidates:

            test_case_id = test_case.test_case_id

            print(
                f"Generating automation for {test_case_id}..."
            )

            try:

                code = self.automation_generator.generate_test(
                    test_case_id
                )

                output_file = (
                    self.automation_generator.save_generated_test(
                        test_case_id,
                        code,
                        user_story_id
                    )
                )

                print(
                    f"Saved: {output_file}"
                )

                generated_files.append(
                    str(output_file)
                )

            except Exception as error:

                print(
                    f"FAILED: {test_case_id}"
                )

                print(
                    f"Reason: {error}"
                )

                continue

        return generated_files

    def process_test_result(self, result):

        for content in result.content:

            if not hasattr(content, "text"):
                continue

            try:
                data = json.loads(content.text)
            except json.JSONDecodeError:
                continue

            failed_tests = [
                test
                for test in data.get("tests", [])
                if test.get("status") == "FAILED"
            ]

            if not failed_tests:
                print("\n===== RESULT =====")
                print("ALL TESTS PASSED")
                return

            print("\n===== FAILED TESTS =====")

            for test in failed_tests:

                print(
                    f"{test.get('test_case_id')} | "
                    f"{test.get('test_name')} | "
                    f"{test.get('test_file')}"
                )

                if test.get("ai_analysis"):
                    print(
                        "\n===== AI FAILURE ANALYSIS ====="
                    )

                    print(
                        test["ai_analysis"]
                    )

    async def run_mcp_tests(self):

        print("\n===== STEP 4: RUNNING TESTS THROUGH MCP =====")

        server_env = os.environ.copy()

        gemini_api_key = os.getenv("GEMINI_API_KEY")

        if gemini_api_key:
            server_env["GEMINI_API_KEY"] = gemini_api_key

        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server.server"],
            env=server_env,
        )

        async with stdio_client(
                server_params
        ) as (read, write):

            async with ClientSession(
                    read,
                    write
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    "run_tests",
                    {}
                )

                print(
                    "\n===== MCP TEST RESULT ====="
                )

                for content in result.content:

                    if hasattr(content, "text"):
                        print(content.text)

                self.process_test_result(result)

                return result

    async def run(self):

        print(
            "\n========================================"
        )

        print(
            "      AI AUTOMATION AGENT"
        )

        print(
            "========================================"
        )

        # =========================================
        # STEP 1: READ USER STORY
        # =========================================

        user_story = self.read_user_story()

        user_story_id = self.extract_user_story_id(
            user_story
        )

        print(
            f"\n===== USER STORY: {user_story_id} ====="
        )

        # =========================================
        # STEP 2: GENERATE TEST CASES
        # =========================================

        test_cases = self.generate_test_cases(
            user_story
        )

        # =========================================
        # STEP 3: APPROVE TEST CASES
        # =========================================

        candidates = self.approve_test_cases(
            test_cases
        )

        # =========================================
        # STEP 4: CLEAN ONLY CURRENT STORY
        # =========================================

        self.prepare_story_generated_folder(
            user_story_id
        )

        # =========================================
        # STEP 5: GENERATE AUTOMATION
        # =========================================

        self.generate_automation(
            candidates,
            user_story_id
        )

        # =========================================
        # STEP 6: RUN ALL TESTS THROUGH MCP
        # =========================================

        mcp_result = await self.run_mcp_tests()

        print(
            "\n===== RAW MCP RESULT RECEIVED ====="
        )

        print(
            mcp_result
        )

        print(
            "\n===== WORKFLOW COMPLETE ====="
        )


async def main():

    agent = AutomationAgent()

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())