import json
from pathlib import Path

from ai.test_generator import TestCaseGenerator


def main():

    # -----------------------------------------
    # 1. Read User Story
    # -----------------------------------------

    user_story_path = Path(
        "test_data/user_story_cart.txt"
    )

    user_story = user_story_path.read_text(
        encoding="utf-8"
    )

    # -----------------------------------------
    # 2. Create Test Case Generator
    # -----------------------------------------

    generator = TestCaseGenerator()

    # -----------------------------------------
    # 3. Send User Story to Gemini
    # -----------------------------------------

    result = generator.generate(
        user_story
    )

    # -----------------------------------------
    # 4. Save ALL generated test cases
    # -----------------------------------------

    output_path = Path(
        "test_data/generated_test_cases.json"
    )

    output_path.write_text(
        json.dumps(
            result.model_dump(),
            indent=2
        ),
        encoding="utf-8"
    )

    # -----------------------------------------
    # 5. Find automation candidates
    # -----------------------------------------

    candidates = generator.get_automation_candidates(
        result
    )

    # -----------------------------------------
    # 6. Print summary
    # -----------------------------------------

    print(
        f"Generated {len(result.test_cases)} test cases."
    )

    print(
        f"Automation candidates: {len(candidates)}"
    )

    print(
        f"Saved to: {output_path}"
    )

    # -----------------------------------------
    # 7. Display automation candidates
    # -----------------------------------------

    print("\nAutomation Candidates:")

    for test_case in candidates:

        print(
            f"- {test_case.test_case_id}: "
            f"{test_case.title}"
        )


if __name__ == "__main__":
    main()
