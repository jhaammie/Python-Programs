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
        d = {"Year":school[1],
              "Is_Preliminary": school[2],
              "Kommun": school[3],
              "Name":school[4],
               "Organisitionsform":school[5],
               "Studievagskod":school[6],
               "Studievag":school[7],
               "Antagningsgrans":school[8],
               "Median":school[9],
              "Antal_platser":school[10],
              "Antagna":school[11],
              "Reserver":school[12],
              "Lediga_platser":school[13]
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
    minMerit = content["minMerit"]
    maxMerit = content["maxMerit"]
    program = content["program"]
    lst = []
    schools = GetGymnasiumWithinRadius(a, b, radius)
#    for a in range(0, len(schools)):
 #       PutMeInLst = schools[a][0]
  #      lst.append(PutMeInLst)

    for school in schools:
        lst.append(school[0])
    DataList = GetDataForSchools(lst, sortby, sortOrder, minMerit, maxMerit, program)
    if len(DataList) > 0:
        print(DataList[0])


    list = []
    for school in DataList:
        d = {"Year":school[1],
              "Is_Preliminary": school[2],
              "Kommun": school[3],
              "Name":school[4],
               "Organisitionsform":school[5],
               "Studievagskod":school[6],
               "Studievag":school[7],
               "Antagningsgrans":school[8],
               "Median":school[9],
              "Antal_platser":school[10],
              "Antagna":school[11],
              "Reserver":school[12],
              "Lediga_platser":school[13]
             }
        list.append(d)
    return list


# Get the data for those schools (l.22)

# Write a join in the getnearestschool function to get you the data which has not just the school names but the other data too.


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
