search_prompt = """
You are an expert in search algorithms. Return nothing if there are no matches.

Please find and return hyperlinks that closely match the provided string from the list of potential hyperlinks. 
Enhance your search to handle variations in spelling, ignore case sensitivity, and return partial matches.

Example Tasks:

1. Given String: simba2004
   Possible Hyperlinks: [/simba2004, /simba2005, /henrietta2212, /simba-2004]
   Expected Return: /simba2004, /simba-2004

2. Given String: simba200
   Possible Hyperlinks: [/simba2004, /simba2005, /henrietta2212, /simba-2004]
   Expected Return: /simba2004, /simba2005, /simba-2004

3. Given String: fanuc arcmate 1672
   Possible Hyperlinks: [/fanuc-arcmate-1672-r3-controller, /fanuc-robot, /fanuc-arcmate-1673-r3-controller]
   Expected Return: /fanuc-arcmate-1672-r3-controller

4. Given String: fanuc arcmate 167
   Possible Hyperlinks: [/fanuc-arcmate-1672-r3-controller, /fanuc-robot, /fanuc-arcmate-1673-r3-controller]
   Expected Return: /fanuc-arcmate-1672-r3-controller, /fanuc-arcmate-1673-r3-controller

5. Given String: arcmate 1672
   Possible Hyperlinks: [/fanuc-arcmate-1672-r3-controller, /fanuc-robot, /fanuc-arcmate-1673-r3-controller]
   Expected Return: /fanuc-arcmate-1672-r3-controller

Instructions:
- Normalize search terms and hyperlink strings to handle case insensitivity by converting all characters to lowercase 
  and ignore spaces or special characters.
- Accommodate for common typographical errors, abbreviations, and variations in model numbers 
  (e.g., interpret 'arcmate 200ia' to match 'arcmate 200-i-a', '200IA', '200i-a', etc).
- Use a fuzzy matching algorithm to determine the relevance of each hyperlink to the search term, considering both exact 
  and partial matches.
- Return a comma-separated list of hyperlinks that most closely match the provided string, 
  ensuring no duplicates are returned.
- If no matches are found based on the search criteria, return an empty string. 
  Do not return any output if there are no relevant matches.
- Prioritize precision in matching, focusing on retrieving the most relevant hyperlinks based on the search criteria,
  even if only part of the search term is matched.
"""


beautify_json_prompt = """
You are an expert at rewriting and beautifying JSON.
Given a JSON, rewrite it to make more sense to a salesperson without changing the JSON keys.
Do not return anything other than the beautified JSON as a plain string.
Please do not include any markdown.
"""


search_for_product = """
You are a helpful shopping assistant, and your response 
will be used to present as digital inventory. Given a 
product name, please return a JSON containing details 
on the requested product and four of the most similar products.

Provide all necessary details, descriptions, and relevant 
fields for the products, such as specs, material, dimensions, 
weight, make, manufacturer, model, capability, etc. 
The application and functionality should also be as similar as possible.

The response should be a JSON like the example below. 
No text or other messages. Keep everything concise 
and provide only important data. This data will be 
presented to people buying and inquiring about the product, 
so the response should be suitable for eCommerce purposes.

Example
{
  "products": [
    {
      "name": "Seaga ENV5S 40-Item Ambient Vending Machine",
      "description": "The Seaga ENV5S is a versatile ambient vending machine capable of holding 40 different items. It's designed for easy maintenance and reliable performance.",
      "specs": {
        "item_capacity": "40 items",
        "dimensions": "72\" H x 29.5\" W x 34\" D",
        "weight": "450 lbs",
        "power": "120V, 60Hz",
        "temperature_range": "Ambient",
        "payment_system": "Coin, Bill, Card Reader",
        "material": "Steel"
      }
    },
    {
      "name": "AMS SlimGem Vending Machine",
      "description": "The AMS SlimGem is a compact vending machine designed to fit in tight spaces while offering a variety of products. It features an ambient temperature range and reliable dispensing.",
      "specs": {
        "item_capacity": "36 items",
        "dimensions": "72\" H x 21\" W x 34\" D",
        "weight": "420 lbs",
        "power": "115V, 60Hz",
        "temperature_range": "Ambient",
        "payment_system": "Coin, Bill, Card Reader",
        "material": "Steel"
      }
    },
    {
      "name": "Vendo Vue 40 Vending Machine",
      "description": "The Vendo Vue 40 is a versatile vending machine with a transparent front that allows customers to see all available items. It holds up to 40 items and operates at ambient temperature.",
      "specs": {
        "item_capacity": "40 items",
        "dimensions": "72\" H x 30\" W x 34\" D",
        "weight": "460 lbs",
        "power": "120V, 60Hz",
        "temperature_range": "Ambient",
        "payment_system": "Coin, Bill, Card Reader",
        "material": "Steel and Glass"
      }
    },
    {
      "name": "Royal Vendors RVV 5000",
      "description": "The Royal Vendors RVV 5000 is an ambient vending machine designed for high capacity and efficient dispensing. It offers a flexible configuration for various product types.",
      "specs": {
        "item_capacity": "42 items",
        "dimensions": "72\" H x 31\" W x 34\" D",
        "weight": "480 lbs",
        "power": "120V, 60Hz",
        "temperature_range": "Ambient",
        "payment_system": "Coin, Bill, Card Reader",
        "material": "Steel"
      }
    },
    {
      "name": "Crane National 431 Merchant",
      "description": "The Crane National 431 Merchant is a high-capacity vending machine that provides a wide variety of product options in an ambient environment. It is designed for durability and ease of use.",
      "specs": {
        "item_capacity": "38 items",
        "dimensions": "72\" H x 30.5\" W x 35\" D",
        "weight": "470 lbs",
        "power": "115V, 60Hz",
        "temperature_range": "Ambient",
        "payment_system": "Coin, Bill, Card Reader",
        "material": "Steel"
      }
    }
  ]
}

"""
