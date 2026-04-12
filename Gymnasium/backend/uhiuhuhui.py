
from hoohoohee import GetCountOfDistinctSchools, GetListOfSchoolNames, InsertSchool
from hehehoohoo import GetCoordinates
import math

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
