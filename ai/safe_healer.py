import re
from pathlib import Path

from ai.models import FailureAnalysis


class SafeHealer:

    def __init__(self, project_root=None):
        self.project_root = Path(project_root or Path.cwd())

    def heal(
        self,
        test_file: str,
        analysis: FailureAnalysis,
        failure_output: str = "",
    ) -> dict:

        result = {
            "healing_attempted": False,
            "healing_applied": False,
            "healing_type": "none",
            "changed_file": None,
            "original_code": None,
            "updated_code": None,
            "reason": None,
        }

        # --------------------------------------------------
        # SAFETY GATE
        # --------------------------------------------------

        if analysis.classification != "Locator Defect":
            result["reason"] = (
                f"Automatic healing is not supported for "
                f"{analysis.classification}"
            )
            return result

        if not analysis.healing_allowed:
            result["reason"] = (
                "AI did not allow automatic healing."
            )
            return result

        if analysis.healing_type != "locator":
            result["reason"] = (
                f"Unsupported healing type: "
                f"{analysis.healing_type}"
            )
            return result

        # --------------------------------------------------
        # ONLY GENERATED TESTS MAY BE MODIFIED
        # --------------------------------------------------

        file_path = Path(test_file)

        if not file_path.is_absolute():
            file_path = self.project_root / file_path

        generated_root = (
            self.project_root
            / "tests"
            / "generated"
        )

        try:
            file_path.resolve().relative_to(
                generated_root.resolve()
            )
        except ValueError:
            result["reason"] = (
                "Safety check failed: only "
                "tests/generated files may be modified."
            )
            return result

        if not file_path.exists():
            result["reason"] = (
                f"Test file not found: {file_path}"
            )
            return result

        original_code = file_path.read_text(
            encoding="utf-8"
        )

        result["healing_attempted"] = True
        result["healing_type"] = "locator"
        result["original_code"] = original_code

        # --------------------------------------------------
        # FIND FAILED LOCATOR
        # --------------------------------------------------

        failed_locator = self._extract_failed_locator(
            failure_output
        )

        if not failed_locator:
            result["reason"] = (
                "Could not identify the failed locator "
                "from pytest output."
            )
            return result

        # --------------------------------------------------
        # FIND AI-RECOMMENDED LOCATOR
        # --------------------------------------------------

        candidate_locator = getattr(
            analysis,
            "replacement_locator",
            None,
        )
        if candidate_locator:
            candidate_locator = candidate_locator.strip()

        if not candidate_locator:
            result["reason"] = (
                "AI analysis did not provide a safe replacement locator."
            )
            return result

        if not candidate_locator:
            result["reason"] = (
                "AI analysis did not provide a safe "
                "replacement locator."
            )
            return result

        # --------------------------------------------------
        # SAFETY CHECKS
        # --------------------------------------------------

        if failed_locator == candidate_locator:
            result["reason"] = (
                "Replacement locator is identical "
                "to the failed locator."
            )
            return result

        if failed_locator not in original_code:
            result["reason"] = (
                "Failed locator was not found in "
                "the test source."
            )
            return result

        occurrences = original_code.count(
            failed_locator
        )

        if occurrences != 1:
            result["reason"] = (
                "Safety check failed: failed locator "
                f"appears {occurrences} times. "
                "Expected exactly one occurrence."
            )
            return result

        # --------------------------------------------------
        # APPLY MINIMAL CHANGE
        # --------------------------------------------------

        healed_code = original_code.replace(
            failed_locator,
            candidate_locator,
            1,
        )

        if healed_code == original_code:
            result["reason"] = (
                "No code change was produced."
            )
            return result

        file_path.write_text(
            healed_code,
            encoding="utf-8",
        )

        result["healing_applied"] = True
        result["changed_file"] = str(
            file_path.relative_to(
                self.project_root
            )
        )
        result["updated_code"] = healed_code
        result["reason"] = (
            "Locator correction applied using "
            "AI diagnosis."
        )

        return result

    # ------------------------------------------------------
    # EXTRACT FAILED LOCATOR FROM PYTEST OUTPUT
    # ------------------------------------------------------

    def _extract_failed_locator(
            self,
            failure_output: str,
    ):
        """
        Extract the exact locator Playwright was waiting for.

        We intentionally read only the Playwright
        'waiting for locator(...)' call-log line.
        """

        match = re.search(
            r'waiting for locator\("(.+?)"\)',
            failure_output,
        )

        if not match:
            return None

        locator = match.group(1)

        # Playwright/pytest escapes quotes inside
        # the locator string.
        locator = locator.replace('\\"', '"')

        return locator

    # ------------------------------------------------------
    # EXTRACT REPLACEMENT FROM AI RECOMMENDATION
    # ------------------------------------------------------

    def _extract_recommended_locator(
            self,
            recommended_action: str,
    ):
        if not recommended_action:
            return None

        # First try to extract a complete data-test selector.
        matches = re.findall(
            r'\[data-test=["\']([^"\']+)["\']\]',
            recommended_action,
        )

        if matches:
            return (
                    '[data-test="'
                    + matches[-1]
                    + '"]'
            )

        # Fallback: Gemini may describe the corrected
        # data-test value in natural language.
        #
        # Example:
        # "append the missing 'k' to 'backpack' in the
        # data-test attribute locator"
        #
        # Example:
        # "change ... to 'add-to-cart-sauce-labs-bike-light'"
        matches = re.findall(
            r"'(add-to-cart-[a-z0-9-]+)'",
            recommended_action,
        )

        if matches:
            return (
                    '[data-test="'
                    + matches[-1]
                    + '"]'
            )

        return None