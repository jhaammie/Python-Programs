

# Brave API
# Error handling

"""

Making a search-engine like thing using brave API
Web search
Image search
Video search
News search

"""

# importing what I need
import requests
import json


UseOptions = input("Would you like to do a web(w), image(i), video(v), or news(n) search? ")
lower = UseOptions.lower()

if lower == 'w':
    # WEB SEARCH

    # Defining a function for web search
    def WebSearch(options, request):

        # My headers
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }

        # Requesting
        req = requests.get(f"https://api.search.brave.com/res/v1/web/search?q={request}", headers=headers)
        data = json.loads(req.text)

        # if the user wants to do a web search
        if options == 1:
            if data and 'web' in data:
                ValuesToRead = 30
                if len(data["web"]["results"]) < 30:
                    ValuesToRead = len(data["web"]["results"])

                # Getting the top 2 results (0 and 1)
                for i in range(0, ValuesToRead):

                    # Parsing the data
                    parsing = data["web"]["results"][i]["url"]
                    print(parsing)

                    parsing2 = data["web"]["results"][i]["description"]
                    print(parsing2)
                    print('\n')

            else:
                print("We couldn't find a result to your request, please try again")

        # or if the user wants to do an image/video search
        elif options == 2:

            # Getting the top two results
            if data and 'videos' in data:
                ValuesToRead = 30
                if len(data["videos"]["results"]) < 30:
                    ValuesToRead = len(data["videos"]["results"])

                for i in range(0, ValuesToRead):

                    # Parsing
                    parsing = data["videos"]["results"][i]["url"]
                    print(i)
                    print(parsing)
                    parsing1 = data["videos"]["results"][i]["thumbnail"]["src"]
                    print(parsing1)
                    print('\n')
            else:
                print("We couldn't find a result to your request, please try again")
    # Asking the user if they would like to do a web search or a video/image search
    op = int(input("Would you like to do a web search (enter 1) or get a video/image search (enter 2)? "))

    # Asking the user for their search query
    req = input("Please enter your query: ")

    # Calling my function
    WebSearch(op, req)

elif lower == "i":

    # IMAGE SEARCH


    def ImageSearch(query):

        # My headers
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }

        # Requesting
        req = requests.get(f"https://api.search.brave.com/res/v1/images/search?q={query}", headers=headers)
        # print(req.text)
        print(req)
        data = json.loads(req.text)
        if data and 'results' in data:
            ValuesToRead = 30
            if len(data["results"]) < 30:
                ValuesToRead = len(data["results"])

            for i in range(0, ValuesToRead):
                parsing = data["results"][i]["url"]
                print("Result: ", i + 1)
                print(parsing)
                print("\n")
        else:
            print("Couldn't get results for your request, please try again")

    request = input("Please enter your query: ")
    ImageSearch(request)

elif lower == "v":

    # VIDEO SEARCH

    def VideoSearch(query):
        # My headers
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }

        # Requesting
        req = requests.get(f"https://api.search.brave.com/res/v1/videos/search?q={query}", headers=headers)
        print(req.text)
        print(req)
        data = json.loads(req.text)

        if data and 'results' in data:
            ValuesToRead = 30
            if len(data["results"]) < 30:
                ValuesToRead = len(data["results"])

            for i in range(0, ValuesToRead):
                parsing = data["results"][i]["url"]
                print("Result: ", i + 1)
                print(parsing)
                print("\n")
        else:
            print("Data could not be found")

    request = input("Please enter your query: ")
    VideoSearch(request)


elif lower == "n":
    # NEWS SEARCH

    def NewsSearch(query):

        # My headers
        headers = {
            'X-Subscription-Token': 'BSAAQhjtyJK48R1VSFGVmZi2ndJ5rE0'
        }

        # Requesting
        req = requests.get(f"https://api.search.brave.com/res/v1/news/search?q={query}", headers=headers)
        print(req.text)
        print(req)
        data = json.loads(req.text)

        if data and 'results' in data:

            ValuesToRead = 30
            if len(data["results"]) < 30:
                ValuesToRead = len(data["results"])
            for i in range(0, ValuesToRead):
                parsing = data["results"][i]["url"]
                print("Result: ", i + 1)
                print(parsing)
                print("\n")
        else:
            print("Data could not be found")

    request = input("Please enter your query: ")
    NewsSearch(request)

else:
    print("Invalid request, please try again")
    quit()
