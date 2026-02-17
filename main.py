import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


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
    
    total_prompt_tokens = 0
    total_response_tokens = 0

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt,
            temperature=0
                )
            )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        else:
            raise Exception("candidate doesn't exist in response")

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response is missing usage metadata")
        
        total_prompt_tokens += response.usage_metadata.prompt_token_count
        total_response_tokens += response.usage_metadata.candidates_token_count
        total_tokens = total_prompt_tokens + total_response_tokens


        function_results = []

        if response.function_calls:
            for function in response.function_calls:
                function_call_result = call_function(function, verbose=args.verbose)
                
                if not function_call_result.parts:
                    raise RuntimeError("No parts in response")
                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError("No function response")
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError("No response data")
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print("Final response:\n" + response.text)
            if args.verbose:
                print(f"Total prompt tokens: {total_prompt_tokens}")
                print(f"Total response tokens: {total_response_tokens}")
                print(f"Total token usage: {total_tokens}")
            break

        messages.append(types.Content(role="user", parts=function_results))
    
    else:
        print("Maximum iteration reached without completing the task")
        sys.exit(1)


if __name__ == "__main__":
    main()