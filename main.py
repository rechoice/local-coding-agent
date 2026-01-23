import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # Load API Key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    # call GenAI module
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    user_prompt = args.user_prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )

    # keep track of token metadata
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:\n", response.text)

if __name__ == "__main__":
    main()