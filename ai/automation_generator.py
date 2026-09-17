import json
from pathlib import Path

from ai.gemini_client import GeminiClient


class AutomationGenerator:

    def __init__(self):

        self.ai = GeminiClient()

        self.project_root = Path(__file__).resolve().parent.parent

    def load_prompt(self):

        prompt_path = (
            self.project_root
            / "prompts"
            / "automation_prompt.txt"
        )

        return prompt_path.read_text(
            encoding="utf-8"
        )

    def load_approved_test_cases(self):

        test_cases_path = (
            self.project_root
            / "test_data"
            / "approved_test_cases.json"
        )

        data = json.loads(
            test_cases_path.read_text(
                encoding="utf-8"
            )
        )

        return data["test_cases"]

    def get_test_case(self, test_case_id):

        test_cases = self.load_approved_test_cases()

        for test_case in test_cases:

            if test_case["test_case_id"] == test_case_id:
                return test_case

        raise ValueError(
            f"Test case not found: {test_case_id}"
        )

    def load_framework_context(self):

        files = [
            "conftest.py",
            "pages/login_page.py",
            "pages/products_page.py",
            "pages/cart_page.py",
            "pages/checkout_page.py",
            "tests/test_cart.py",
        ]

        context_parts = []

        for file_name in files:

            file_path = self.project_root / file_name

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Framework file not found: {file_path}"
                )

            content = file_path.read_text(
                encoding="utf-8"
            )

            context_parts.append(
                f"\n===== {file_name} =====\n"
                f"{content}\n"
            )

        return "\n".join(context_parts)

    def build_prompt(self, test_case):

        prompt_template = self.load_prompt()

        framework_context = (
            self.load_framework_context()
        )

        test_case_json = json.dumps(
            test_case,
            indent=2
        )

        prompt = prompt_template.replace(
            "{{TEST_CASE}}",
            test_case_json
        )

        prompt = prompt.replace(
            "{{FRAMEWORK_CONTEXT}}",
            framework_context
        )

        return prompt

    def clean_generated_code(self, generated_code):

        code = generated_code.strip()

        if code.startswith("```python"):
            code = code[len("```python"):].strip()

        elif code.startswith("```"):
            code = code[len("```"):].strip()

        if code.endswith("```"):
            code = code[:-3].strip()

        return code

    def generate_test(self, test_case_id):

        test_case = self.get_test_case(
            test_case_id
        )

        prompt = self.build_prompt(
            test_case
        )

        generated_code = self.ai.generate_automation(
            prompt
        )

        generated_code = self.clean_generated_code(
            generated_code
        )

        return generated_code

    def save_generated_test(
            self,
            test_case_id,
            generated_code,
            user_story_id
    ):

        output_directory = (
                self.project_root
                / "tests"
                / "generated"
                / user_story_id
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
                output_directory
                / f"test_{test_case_id}.py"
        )

        output_file.write_text(
            generated_code,
            encoding="utf-8"
        )

        return output_file

