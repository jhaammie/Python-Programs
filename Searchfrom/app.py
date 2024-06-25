
# Importing everything I need (what's render_template?)
from flask import Flask, request, render_template
from flask_cors import CORS
import requests

# Defining variable 'app'
app = Flask(__name__)  # Creates an instance of app
CORS(app)


# Using app as a decorator and defining the methods I'd be using (A decorator is to call a function
# in another manner right? What does the / signify?)


@app.route('/', methods=["GET", "POST"])
# Creating a function to search images
def search_images():
    # if the request method is post
    if request.method == "POST":

        query = request.form["query"]

        # My headers to call the API, the only required one is the subscription
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }

        # url for brave api
        url = f"https://api.search.brave.com/res/v1/images/search?q={query}"

        # Using the get method to call the api
        response = requests.get(url, headers=headers)

        # Converting response to json
        data = response.json()

        # Defining an empty list called 'results'
        results = []

        # If the key 'results' is in data
        if data and "results" in data:

            # Starting a for loop which is...? Doing what?
            for result in data["results"]:
                # Explanation required (Is it like saying 'url' when run?)
                url = result.get("url", "")

                # Explanation required (Is it like saying 'title' when run?)
                title = result.get("title", "")

                # Appending the above into the 'results' list
                results.append({"url": url, "title": title})

        return render_template("search_results.html", results=results)

    return render_template("index.html")


# Running the app on my device
if __name__ == "__main__":  # https://www.geeksforgeeks.org/__name__-a-special-variable-in-python/
    app.run(debug=True, host='0.0.0.0')
