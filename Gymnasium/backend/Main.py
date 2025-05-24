from flask import Flask, request
from flask_cors import CORS
from hoohoohee import GetNearestSchools, GetDataForSchools, GetGymnasiumWithinRadius

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
    lst = []
    schools = GetGymnasiumWithinRadius(a, b, radius)
#    for a in range(0, len(schools)):
 #       PutMeInLst = schools[a][0]
  #      lst.append(PutMeInLst)

    for school in schools:
        lst.append(school[0])
    DataList = GetDataForSchools(lst, sortby, sortOrder, minpreMerit, minfinMerit, maxpreMerit, maxfinMerit, programs, year)
    if len(DataList) > 0:
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


# Get the data for those schools (l.22)

# Write a join in the getnearestschool function to get you the data which has not just the school names but the other data too.


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)
