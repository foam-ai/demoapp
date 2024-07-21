import json
import os
from openai import OpenAI
from app.prompts import beautify_json_prompt, search_for_product


# Access the API key from an environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key from the environment
client = OpenAI(api_key="sk-proj-8puDYhZcqpSIZkl4wmHxT3BlbkFJ6q3UZvpd6ZDx2xBWt9JK")


def clean_product_open_ai(prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        {"role": "system", "content": search_for_product},
        {"role": "user", "content": prompt}
    ]
    )
    content = completion.choices[0].message.content
    print("CONTENT", content)
    return content


def call_open_ai(prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        {"role": "system", "content": search_for_product},
        {"role": "user", "content": prompt}
    ]
    )
    content = completion.choices[0].message.content
    print("CONTENT", content)
    return content


def call_perplexity(prompt: str):
    YOUR_API_KEY = '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'
    BASE_URL = "https://api.perplexity.ai"
    pplx_client = OpenAI(api_key=YOUR_API_KEY, base_url=BASE_URL)
    completion = pplx_client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=[
        {"role": "system", "content": search_for_product},
        {"role": "user", "content": prompt}
    ]
    )
    content = completion.choices[0].message.content
    print("CONTENT", content)
    return content


def call_open_ai_hyperlinks(prompt, search_term, links):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"String: {search_term}\nHyperlinks: {', '.join(links)}"}
        ]
    )
    content = completion.choices[0].message.content
    return content


def call_open_ai_rewrite_json():
    try:
        with open('output.json', 'r') as file:
            json_input = json.load(file)
    except json.JSONDecodeError:
        print("Error: output.json is empty or contains invalid JSON.")
        return

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": beautify_json_prompt},
            {"role": "user", "content": f"Input JSON: {json.dumps(json_input)}"}
        ]
    )
    content = completion.choices[0].message.content.strip()
    try:
        beautified_json = json.loads(content)
    except json.JSONDecodeError:
        print("Error: OpenAI response is not valid JSON.")
        return

    with open('output.json', 'w') as file:
        json.dump(beautified_json, file, indent=4)


def call_open_ai_extract_fields(data):
    prompt = (
        "You are an expert at extracting and rewording data. Given the following string, "
        "extract the relevant information and return a JSON object with the fields: "
        "condition, mounting, axes, reach, payload, quantity, title, price, a reworded shorter "
        "and better description, weight, url, and extra_information. The extra_information value should be a string."
        "It provide only a summary of any extra information that would be useful. payload and capacity are the same."
        "Please use all of the data provided to you to. The result should be normalized."
        "provide me with a JSON with all fields. If a field is not available, please mark it as N/A."
        "Here is an example of the input string:\n"
        "\n"
        "URL: http://example.com\n"
        "Title: FANUC ARCMATE 120i MIG WELDING ROBOT RJ3 CONTROLLER\n"
        "Price: Contact us for price\n"
        "Available Quantity: 1\n"
        "Specifications:\n"
        "Condition: Used\n"
        "Axes: 6\n"
        "Payload: 16kg\n"
        "H-Reach: 1542mm\n"
        "Robot Mass: 370kg\n"
        "Structure: Articulated\n"
        "Mounting: Floor, Inverted, Angle\n"
        "Description: 1-FANUC ARCMATE 120i 6 AXIS MIG WELDING ROBOT WITH LINCOLN WIRE & TORCH ..."
        "\n\n"
        "Example of the output JSON:\n"
        "{\n"
        "  'condition': 'Used',\n"
        "  'mounting': 'Floor, Inverted, Angle',\n"
        "  'axes': '6',\n"
        "  'reach': '1542mm',\n"
        "  'payload': '16kg',\n"
        "  'quantity': '1',\n"
        "  'title': 'FANUC ARCMATE 120i MIG WELDING ROBOT RJ3 CONTROLLER',\n"
        "  'price': 'N/A',\n"
        "  'description': 'A 6-axis MIG welding robot with a Lincoln wire and torch, suitable for "
        "   various welding applications.',\n"
        "  'weight': '370kg',\n"
        "  'url': 'http://example.com',\n"
        "  'extra_information': 'FANUC ARCMATE 120i is a reliable and widely used robot model compatible"
        "   with RJ3 controllers.'\n"
        "}"
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"String: {data}"}
        ],
    )
    content = completion.choices[0].message.content.replace("```json", "").replace("```", "")
    return json.loads(content)


def call_open_ai_calculate_relevance(search_term, result):
    prompt = (f"Given the query '{search_term}', determine if the result is valid and relevant. "
              f"Respond with 'valid' or 'invalid'. Please do not provide an explanation simply return"
              f"'valid' or 'invalid'")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Result: {result}"}
        ]
    )
    content = completion.choices[0].message.content
    return content
