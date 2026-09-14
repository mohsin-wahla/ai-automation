import os

from google import genai
from google.genai import types


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3-flash-preview"

    def generate_test_cases(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "test_cases": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "test_case_id": {
                                        "type": "STRING"
                                    },
                                    "title": {
                                        "type": "STRING"
                                    },
                                    "type": {
                                        "type": "STRING"
                                    },
                                    "priority": {
                                        "type": "STRING"
                                    },
                                    "preconditions": {
                                        "type": "ARRAY",
                                        "items": {
                                            "type": "STRING"
                                        }
                                    },
                                    "steps": {
                                        "type": "ARRAY",
                                        "items": {
                                            "type": "STRING"
                                        }
                                    },
                                    "test_data": {
                                        "type": "OBJECT"
                                    },
                                    "expected_result": {
                                        "type": "ARRAY",
                                        "items": {
                                            "type": "STRING"
                                        }
                                    },
                                    "automation_candidate": {
                                        "type": "BOOLEAN"
                                    }
                                },
                                "required": [
                                    "test_case_id",
                                    "title",
                                    "type",
                                    "priority",
                                    "preconditions",
                                    "steps",
                                    "test_data",
                                    "expected_result",
                                    "automation_candidate"
                                ]
                            }
                        }
                    },
                    "required": [
                        "test_cases"
                    ]
                }
            )
        )

        return response.text

    def generate_automation(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="text/plain"
            )
        )


        return response.text or ""

    # def generate_automation(self, prompt: str) -> str:
    #
    #     response = self.client.models.generate_content(
    #         model=self.model,
    #         contents=prompt,
    #         config=types.GenerateContentConfig(
    #             response_mime_type="text/plain"
    #         )
    #     )
    #
    #     return response.text
