import http.client
import urllib.parse
import json

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

"""latitude, longitude = GetCoordinates("JENSEN grundskola Sickla")
print("latitude:", latitude, "longitude:", longitude)"""



# HOMEWORK: CONVERT ABOVE TO A FUNCTION WHICH TAKES IN PLACE AS AN INPUT AND OUTPUTS THE LATITUDE AND LONGITUDE
# WRITE ANOTHER FUNCTION WHICH
# 1. GETS THE COUNT OF DISTINCT SCHOOLS IN THE TABLE GYMNASIUM
# 2. WRITE FORMULA TO COUNT THE NUMBER OF PAGES (WRITE IT IN CODE)
# 3. FOR EVERY PAGE GET THE LIST OF SCHOOLS
# 4. FOR EVERY SCHOOL GET LAT AND LONG BY CALLING THE FUNCTION YOU JUST WROTE EARLIER
# 5. INSERT THE SCHOOL NAME, LAT, LONG INTO THE TABLE SCHOOL
