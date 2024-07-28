import json
import os
from openai import OpenAI


class ChatGPTClient:
    def __init__(self):
        # Access the API key from an environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        # Initialize the OpenAI client with the API key from the environment
        self.client = OpenAI(api_key=api_key)

    def analyze(self, content, system_content=''):

        completion = self.client.chat.completions.create(
            model="gpt-4o",  # Note: Changed from "gpt-4o" to "gpt-4" as "gpt-4o" is not a standard model name
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": content}
            ]
        )
        response_content = completion.choices[0].message.content
        print("CONTENT", response_content)
        return response_content

    def analyze_json(self, content):
        response = self.analyze(content)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print("Failed to parse response as JSON. Returning raw string.")
            return response


# Example usage
if __name__ == "__main__":
    chatgpt_client = ChatGPTClient()

    # Example of using the search prompt
    search_result = chatgpt_client.analyze("Looking for a smartphone with good camera")
    print("Search Result:", search_result)

    # Example of using the beautify JSON prompt
    json_data = '{"name": "John", "age": 30}'
    beautified_json = chatgpt_client.analyze_json(json_data)
    print("Beautified JSON:", json.dumps(beautified_json, indent=2))
