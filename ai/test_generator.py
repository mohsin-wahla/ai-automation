import json
from pathlib import Path

from ai.gemini_client import GeminiClient
from ai.models import TestCaseCollection


class TestCaseGenerator:

    def __init__(self):
        self.ai = GeminiClient()

    def load_prompt(self):

        prompt_path = Path(
            "prompts/test_case_prompt.txt"
        )

        return prompt_path.read_text(
            encoding="utf-8"
        )

    def generate(self, user_story: str):

        prompt_template = self.load_prompt()

        prompt = prompt_template.replace(
            "{{USER_STORY}}",
            user_story
        )

        response = self.ai.generate(prompt)

        data = json.loads(response)

        validated_data = TestCaseCollection.model_validate(
            data
        )

        return validated_data

    def get_automation_candidates(
            self,
            test_cases: TestCaseCollection
    ):
        return [
            test_case
            for test_case in test_cases.test_cases
            if test_case.automation_candidate
        ]

