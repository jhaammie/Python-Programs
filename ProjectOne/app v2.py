from flask import Flask, request, make_response
import requests

app1 = Flask(__name__)


@app1.route('/', methods=["GET", "POST"])
def search_images():
    if request.method == "POST":
        query = request.form["query"]
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }
        url = f"https://api.search.brave.com/res/v1/images/search?q={query}"
        response = requests.get(url, headers=headers)
        data = response.json()

        with open("templates/search_results.html", "r") as f:
            html_template = f.read()

        if data.get("results"):
            result_html = "".join([f'<div><img src="{result["url"]}" alt="{result["title"]}" width="300"><p>{result["title"]}</p></div>' for result in data["results"]])
        else:
            result_html = "<p>No results found.</p>"

        html_content = html_template.replace("{{ results }}", result_html)
        response = make_response(html_content)
        response.headers["Content-Type"] = "text/html"
        return response

    with open("templates/index.html", "r") as f:
        html_content = f.read()
    response = make_response(html_content)
    response.headers["Content-Type"] = "text/html"
    return response


if __name__ == "__main__":
    app1.run(debug=True)
