import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Send a prompt to the chatbot.")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENROUTER_API_KEY in the project's .env file before running.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if response.usage is None:
            raise RuntimeError("The API response did not include token usage information.")
        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"Final response:\n{message.content}")
            return

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise Exception("Function call returned an empty result")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    print("Error: agent loop reached the maximum number of iterations without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
