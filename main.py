import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # Load configuration
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = args.user_prompt
    
    # Represent the conversation as a list of structured messages (multi-turn ready)
    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=user_prompt)],
            )
        ]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    # Ensure the response contains token usage metadata
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if args.verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:\n", response.text)
    print("Response:\n", response.text)


if __name__ == "__main__":
    main()