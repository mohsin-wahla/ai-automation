
from ai.gemini_client import GeminiClient


class FailureAnalyzer:

    def __init__(self):
        self.ai = GeminiClient()

    def analyze(
        self,
        test_name: str,
        error_message: str,
        test_code: str
    ) -> str:

        prompt = f"""
You are a Senior QA Automation Engineer.

Analyze the following Playwright + Pytest automation failure.

TEST NAME:
{test_name}

TEST CODE:
```python
{test_code}

ERROR / FAILURE:

{error_message}

Provide a concise analysis with exactly these sections:

FAILURE
LIKELY ROOT CAUSE
EVIDENCE
RECOMMENDED ACTION
Rules:

Do not modify the test.

Do not generate replacement code.

Do not invent application behavior.

Base the analysis only on the provided test code and failure.

Clearly distinguish between confirmed evidence and likely root cause.

Keep the analysis concise and practical for a QA automation engineer.
"""

        return self.ai.generate_automation(prompt)