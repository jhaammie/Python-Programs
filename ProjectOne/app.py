"""



"""

# Importing everything I need (what's render_template?)
from flask import Flask, request, render_template
import requests

# Defining variable 'app' (what does __name__ mean?)
app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello():
    name = request.args.get('name', 'world')
    return f"Hello {name}"


@app.route('/add', methods=["GET"])
def add():
    n1 = request.args.get('n1')
    n2 = request.args.get('n2')
    sum = int(n1) + int(n2)
    return str(sum)


"""
# Using app as a decorator and defining the methods I'd be using (A decorator is to call a function
# in another manner right? What does the / signify?)


@app.route('/search', methods=["GET", "POST"])
# Creating a function to search images
def search_images():
    # if the request method is post
    if request.method == "POST":

        # ?????? WELP
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

        # Explanation required
        return render_template("search_results.html", results=results)

    # Explanation required
    return render_template("index.html")

"""
# Explanation required
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

"""
import requests
from flask import Flask, request, render_template

app = Flask(__name__)


# Define the root route for displaying the search form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Define a route for processing the search query
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # My headers
    headers = {
        'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
    }

    # Call your API to perform the web search
    api_url = f"https://api.search.brave.com/res/v1/images/search"
    response = requests.get(api_url, params={'query': query}, headers=headers)
    # Process the response from the API
    if response.status_code == 200:
        search_results = response.json()
        # Here you can further process the search results as needed
        # For this example, we'll simply return the search results
        return render_template('search_results.html', results=search_results)
    else:
        return f'Error: Unable to perform the search'


if __name__ == '__main__':
    app.run(debug=True)

"""

"""
# Importing what I need
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello():
    return "Hi World"


"""

"""
from flask import Flask
import requests
# Creating the app instance, and using it to handle incoming web requests and send responses to the user.
app = Flask(__name__)  # The variable __name__ holds the name of the current Python module


@app.route('/', methods=["GET"])
def hello():
    request = input("Please enter your query: ")
    headers = {
        'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
    }

    # Requesting
    req = requests.get(f"https://api.search.brave.com/res/v1/images/search?q={request}", headers=headers)



from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def search_images():
    if request.method == "POST":
        query = request.form["query"]
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }
        url = f"https://api.search.brave.com/res/v1/images/search?q={query}"
        response = requests.get(url, headers=headers)
        data = response.json()
        return render_template_string("search_results.html", data=data)
    return render_template_string("index.html")


if __name__ == "__main__":
    app.run(debug=True)
"""
