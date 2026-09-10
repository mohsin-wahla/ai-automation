from ai.gemini_client import GeminiClient

def test_gemini_connection():

    gemini = GeminiClient()

    response = gemini.generate(
        "Explain Playwright in one sentence."
    )

    print(response)

    assert response