from ai.automation_generator import AutomationGenerator


def main():

    test_case_id = "TC-US002-03"

    generator = AutomationGenerator()

    print(
        f"Generating automation for {test_case_id}..."
    )

    generated_code = generator.generate_test(
        test_case_id
    )

    output_file = generator.save_generated_test(
        test_case_id,
        generated_code
    )

    print(
        "\nAutomation generated successfully."
    )

    print(
        f"Saved to: {output_file}"
    )


if __name__ == "__main__":
    main()
