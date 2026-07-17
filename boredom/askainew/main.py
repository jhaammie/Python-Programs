import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from mistralai.client import Mistral

app = Flask(__name__)

CORS(app)


@app.route("/question", methods=["POST"])
def apicall():
    data = request.get_json()
    print(data.get("question"))

    endpoint = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {"VL6RwunL4EsW6CQPAUfH00o3u445QajQ"}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-medium",
        "messages": [
            {"role": "user", "content": f"{data.get("question")}"}
        ],
        "temperature": 0.7  # Optional: controls randomness (0.0 to 1.0)
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        a = result["choices"][0]["message"]["content"]  # Print the AI's response
    else:
        a = f"Error: {response.status_code}, {response.text}"

    dictionary =  {"answerinjson":a}

    return dictionary


if __name__ == '__main__':
    app.run(debug=True)

