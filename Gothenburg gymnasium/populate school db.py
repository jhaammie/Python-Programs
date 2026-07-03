import http.client
import urllib.parse
import json

from db import GetCountOfDistinctSchools, GetListOfSchoolNames, InsertSchool
import math

def GetCoordinates(place):

    place = urllib.parse.quote(place)
    conn = http.client.HTTPSConnection("maps-data.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "f246e465b3msha3b9540d4b134b0p16918bjsn84e730ab6b3d",
        'x-rapidapi-host': "maps-data.p.rapidapi.com"
    }
    conn.request("GET", f"/geocoding.php?query={place}&lang=en&country=se", headers=headers)

    res = conn.getresponse()
    data = res.read()

    response = data.decode("utf-8")

    response = json.loads(response)
    if response and 'data' in response:
        latitude = response["data"]["lat"]
        longitude = response["data"]["lng"]
        return latitude, longitude
    return None, None


def PopulateLocation():
    TotalNumberOfSchools = GetCountOfDistinctSchools()
    PageSize = 100
    TotalNumberOfPages = TotalNumberOfSchools / PageSize
    TotalNumberOfPages = math.ceil(TotalNumberOfPages)
    for PageNumber in range(TotalNumberOfPages):
        ListOfSchools = GetListOfSchoolNames(PageNumber, PageSize)
        for school in ListOfSchools:
            latitude, longitude = GetCoordinates(school[0])
            if latitude is not None:
                InsertSchool(school[0], latitude, longitude)
            else:
                print(f"Latty and Longy for {school[0]} were not foundddddddddddd")

PopulateLocation()
