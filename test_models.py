"""List available Gemini models (development utility)."""

from google import genai

from app.config import GEMINI_API_KEY


def main():
    client = genai.Client(api_key=GEMINI_API_KEY)

    for model in client.models.list():
        print(model.name)


if __name__ == "__main__":
    main()
