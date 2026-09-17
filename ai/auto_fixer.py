from ai.gemini_client import GeminiClient


class AutoFixer:

    def __init__(self):
        self.ai = GeminiClient()

    def fix_test(
        self,
        test_name: str,
        test_code: str,
        error_message: str,
        analysis: str
    ) -> str:

        prompt = f"""
You are a Senior QA Automation Engineer specializing in
Playwright + Pytest self-healing automation.

A generated Playwright test has failed.

TEST NAME:
{test_name}

CURRENT TEST CODE:
{test_code}

FAILURE:
{error_message}

AI FAILURE ANALYSIS:
{analysis}

Your task is to fix ONLY the test automation code.

Rules:

Return ONLY valid Python code.
Do not return markdown fences.
Do not explain anything.
Do not change the intended test behavior.
Do not invent application behavior.
Preserve existing Page Objects and fixtures.
Make the smallest possible correction.
The returned code must be a complete replacement for the current test file.
Do not modify unrelated tests.
Ensure the resulting code is valid Playwright + Pytest code.
Return the corrected complete test file.
"""

        return self.ai.generate_automation(prompt)
