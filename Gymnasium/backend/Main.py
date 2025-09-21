from flask import Flask, request
from flask_cors import CORS
from hoohoohee import GetNearestSchools, GetDataForSchools, GetPaginatedDataForSchools, SearchSchoolsByName, \
    GetSchoolDetails

app = Flask(__name__)  # Creates an instance of app
CORS(app)

@app.route('/health-check', methods=["GET"])
def HealthCheck():
    return "OK"

@app.route('/gymnasium', methods=["POST"])
def GetNearestGymnasium():
    content = request.json
    a = content["latitude"]
    b = content["longitude"]
    count = 10
    lst = []
    schools = GetNearestSchools(a, b, count)
#    for a in range(0, len(schools)):
 #       PutMeInLst = schools[a][0]
  #      lst.append(PutMeInLst)

    for school in schools:
        lst.append(school[0])
    DataList = GetDataForSchools(lst, None, None)
    print(DataList[0])
    list = []
    for school in DataList:
        d = {"Year":school[0],
               "Kommun": school[1],
               "Name":school[2],
               "Organisitionsform":school[3],
               "Studievagskod":school[4],
               "Studievag":school[5],
               "Antagningsgrans_prelim":school[6],
               "Antagningsgrans_final": school[7],
               "Median_prelim":school[8],
               "Median_final": school[9],
               "Antal_platser_prelim":school[10],
               "Antal_platser_final": school[11],
               "Antagna_prelim":school[12],
               "Antagna_final": school[13],
               "Reserver_prelim":school[14],
               "Reserver_final": school[15],
               "Lediga_platser_prelim":school[16],
               "Lediga_platser_final": school[17],
                "grans_diff":school[18],
                "median_diff":school[19]

             }

        list.append(d)
    return list

@app.route('/gymnasium-within-radius', methods=["POST"])
def GymnasiumWithinRadius():

    content = request.json
    a = content["latitude"]
    b = content["longitude"]
    radius = content["radius"]
    sortby = content["sortBy"]
    sortOrder = content["sortOrder"]
    minpreMerit = content["minpreMerit"]
    maxpreMerit = content["maxpreMerit"]
    minfinMerit = content["minfinMerit"]
    maxfinMerit = content["maxfinMerit"]
    programs = content["programs"]
    year = content["year"]
    pageno = content["pageno"]
    pagesize = content["pagesize"]

    DataList = GetPaginatedDataForSchools(a, b, radius, pageno, pagesize, sortby, sortOrder, minpreMerit, minfinMerit, maxpreMerit, maxfinMerit, programs, year)
    list = []
    for school in DataList:
        d = {"Year":school[0],
              "Kommun": school[1],
              "Name":school[2],
               "Organisitionsform":school[3],
               "Studievagskod":school[4],
               "Studievag":school[5],
               "Antagningsgrans_prelim":school[6],
               "Antagningsgrans_final": school[7],
               "Median_prelim":school[8],
               "Median_final": school[9],
               "Antal_platser_prelim":school[10],
               "Antal_platser_final": school[11],
               "Antagna_prelim":school[12],
               "Antagna_final": school[13],
               "Reserver_prelim":school[14],
               "Reserver_final": school[15],
               "Lediga_platser_prelim":school[16],
               "Lediga_platser_final": school[17],
                "grans_diff":school[18],
                "median_diff":school[19]
             }
        list.append(d)
    return list

@app.route('/gymnasium/search', methods=["GET"])
def gymnasiumSearch():
    lst = []
    SearchQuery = request.args.get('search_query')
    SearchQuery = SearchQuery.strip()
    result = SearchSchoolsByName(SearchQuery)
    for i in result:
        d = {"name": i[0],
             "id": i[1]}
        lst.append(d)
    return lst

# Get the data for those schools (l.22)

# Write a join in the getnearestschool function to get you the data which has not just the school names but the other data too.


@app.route('/gymnasium/details', methods=["POST"])
def GetGymnasiumDetails():
    content = request.json
    id = content["id"]
    if id.isnumeric():
        data = GetSchoolDetails(id)
        response = {}
        response["id"] = data[0][0]
        response["name"] = data[0][1]
        response["latitude"] = data[0][2]
        response["longitude"] = data[0][3]
        response["kommun"] = data[0][6]
        response["score"] = []
        for i in data:
            score = {}
            score["year"] = i[5]
            score["organisationsform"] = i[8]
            score["studievägskod"] = i[9]
            score["Studievag"] = i[10]
            score["Antagningsgrans_prelim"] = i[11]
            score["Antagningsgrans_final"] = i[12]
            score["Median_prelim"] = i[13]
            score["Median_final"] = i[14]
            score["Antal_platser_prelim"] = i[15]
            score["Antal_platser_final"] = i[16]
            score["Antagna_prelim"] = i[17]
            score["Antagna_final"] = i[18]
            score["Reserver_prelim"] = i[19]
            score["Reserver_final"] = i[20]
            score["Lediga_platser_prelim"] = i[21]
            score["Lediga_platser_final"] = i[22]

            response["score"].append(score)
        print(data[0])

        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)
