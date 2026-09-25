from ai.gemini_client import GeminiClient
from ai.models import FailureAnalysis


class FailureAnalyzer:

    def __init__(self):
        self.ai = GeminiClient()

    def analyze(
        self,
        test_name: str,
        error_message: str,
        test_code: str,
    ) -> FailureAnalysis:

        prompt = f"""
You are a Senior QA Automation Engineer.

Analyze this failed Python + Playwright + Pytest test.

Your job is diagnosis only.

DO NOT modify the test.
DO NOT generate replacement code.

You MAY provide the exact corrected locator in the
replacement_locator field when automatic locator healing
is allowed.

Classify the failure into exactly ONE category:

- Test Defect
- Application Defect
- Locator Defect
- Assertion Defect
- Test Data Defect
- State Isolation Defect
- Environment/Execution Defect
- Duplicate/Stale Test
- AI Generation Defect
- Unknown

Rules:

1. Use only the supplied test code and failure output.
2. Do not invent application behavior.
3. A failed test is NOT automatically an Application Defect.
4. If Playwright reports that a locator does not exist,
   investigate whether it is a Locator Defect.
5. If Playwright strict mode reports multiple elements,
   investigate whether the locator is too generic.
6. If the test performs one action but expects a different
   result, consider Assertion Defect.
7. NEVER recommend changing the expected value merely to
   match the actual value.
8. healing_allowed can ONLY be true for a clearly identified
   scripting-side locator defect that is safe to automatically repair.

9. Assertion Defect must have healing_allowed = false.

10. Application Defect must have healing_allowed = false.

11. Unknown must have healing_allowed = false.

12. If healing is allowed, healing_type must be "locator".

13. Otherwise healing_type must be "none".

14. If healing_allowed is true, replacement_locator MUST contain
    the complete corrected Playwright locator.

15. For data-test locators, replacement_locator MUST use this format:
    [data-test="exact-value"]

16. replacement_locator must contain ONLY the locator.
    Do not put explanations, markdown, or code around it.

17. If healing_allowed is false, replacement_locator must be
    an empty string.

TEST NAME:
{test_name}

FAILURE OUTPUT:
{error_message}

TEST CODE:
{test_code}
"""

        result = self.ai.generate_failure_analysis(prompt)

        return FailureAnalysis.model_validate_json(result)