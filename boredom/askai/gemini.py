import requests
def askgemini(text):
    # 1. Use a production model version
    model = "gemini-3.1-flash-lite"

    # 2. Provide the API key as a query parameter (?key=YOUR_KEY)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    # 3. Standard headers
    headers = {"Content-Type": "application/json", "X-goog-api-key":"AQ.Ab8RN6It_l-OYjZT23-aCx0Gv8434F3AowJQt6OaM6LABQkU5A"}

    # 4. Correct payload structure
    payload = {"contents": [{"parts": [{"text": text}]}]}

    # 5. Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check for HTTP errors
    if response.status_code == 200:
        # Safely parse and print the text response from the JSON payload
        result = response.json()
        try:
            res = (result["candidates"][0]["content"]["parts"][0]["text"])
            return res
        except (KeyError, IndexError):
            return "Unexpected JSON structure:", result
    else:
        print(f"Error {response.status_code}: {response.text}")
