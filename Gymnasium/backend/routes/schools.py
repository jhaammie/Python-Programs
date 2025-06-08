from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from hoohoohee import GetSchoolById, GetSchoolsInRadius, GetSchoolPredictions, GetSchoolHistoricalData, GetSchoolLocation, GetGymnasiumWithinRadius, GetDataForSchools, PredictSchoolsWithinRadius
from .auth import get_current_user

router = APIRouter()

class SchoolBase(BaseModel):
    Year: int
    Kommun: str
    Name: str
    Organisitionsform: str
    Studievagskod: str
    Studievag: str
    Antagningsgrans_prelim: float
    Antagningsgrans_final: float
    Median_prelim: float
    Median_final: float
    Antal_platser_prelim: int
    Antal_platser_final: int
    Antagna_prelim: int
    Antagna_final: int
    Reserver_prelim: int
    Reserver_final: int
    Lediga_platser_prelim: int
    Lediga_platser_final: int
    grans_diff: float
    median_diff: float

class PaginatedResponse(BaseModel):
    data: List[SchoolBase]
    total: int
    page: int
    pageSize: int
    totalPages: int

class SchoolLocation(BaseModel):
    latitude: float
    longitude: float

class SchoolDetails(BaseModel):
    historical_data: List[SchoolBase]
    location: SchoolLocation

class SchoolPrediction(SchoolBase):
    latitude: float
    longitude: float
    distance: float

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius: float
    year: int
    prelim_score: float
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    minpreMerit: Optional[float] = None
    maxpreMerit: Optional[float] = None
    minfinMerit: Optional[float] = None
    maxfinMerit: Optional[float] = None
    programs: Optional[List[str]] = None
    page: Optional[int] = 0
    pageSize: Optional[int] = 50

@router.get("/schools/{school_name}", response_model=SchoolDetails)
async def get_school_details(school_name: str, current_user: int = Depends(get_current_user)):
    historical_data = GetSchoolHistoricalData(school_name)
    location = GetSchoolLocation(school_name)
    
    formatted_data = []
    for row in historical_data:
        d = {
            "Year": row[0],
            "Kommun": row[1],
            "Name": row[2],
            "Organisitionsform": row[3],
            "Studievagskod": row[4],
            "Studievag": row[5],
            "Antagningsgrans_prelim": row[6],
            "Antagningsgrans_final": row[7],
            "Median_prelim": row[8],
            "Median_final": row[9],
            "Antal_platser_prelim": row[10],
            "Antal_platser_final": row[11],
            "Antagna_prelim": row[12],
            "Antagna_final": row[13],
            "Reserver_prelim": row[14],
            "Reserver_final": row[15],
            "Lediga_platser_prelim": row[16],
            "Lediga_platser_final": row[17],
            "grans_diff": row[18],
            "median_diff": row[19]
        }
        formatted_data.append(d)
    
    return {
        "historical_data": formatted_data,
        "location": {
            "latitude": location[0] if location else None,
            "longitude": location[1] if location else None
        }
    }

@router.post("/schools/nearby", response_model=PaginatedResponse)
async def get_nearby_schools(
    location: LocationRequest,
    current_user: int = Depends(get_current_user)
):
    schools, total_count = GetGymnasiumWithinRadius(
        location.latitude,
        location.longitude,
        location.radius,
        location.page,
        location.pageSize
    )
    
    school_names = [school[0] for school in schools]
    data_list = GetDataForSchools(
        school_names,
        location.sortBy,
        location.sortOrder,
        location.minpreMerit,
        location.minfinMerit,
        location.maxpreMerit,
        location.maxfinMerit,
        location.programs,
        location.year
    )
    
    result = []
    for school in data_list:
        d = {
            "Year": school[0],
            "Kommun": school[1],
            "Name": school[2],
            "Organisitionsform": school[3],
            "Studievagskod": school[4],
            "Studievag": school[5],
            "Antagningsgrans_prelim": school[6],
            "Antagningsgrans_final": school[7],
            "Median_prelim": school[8],
            "Median_final": school[9],
            "Antal_platser_prelim": school[10],
            "Antal_platser_final": school[11],
            "Antagna_prelim": school[12],
            "Antagna_final": school[13],
            "Reserver_prelim": school[14],
            "Reserver_final": school[15],
            "Lediga_platser_prelim": school[16],
            "Lediga_platser_final": school[17],
            "grans_diff": school[18],
            "median_diff": school[19]
        }
        result.append(d)
    
    return {
        "data": result,
        "total": total_count,
        "page": location.page,
        "pageSize": location.pageSize,
        "totalPages": (total_count + location.pageSize - 1) // location.pageSize
    }

@router.post("/schools/predictions", response_model=List[SchoolPrediction])
async def get_school_predictions(
    location: LocationRequest,
    current_user: int = Depends(get_current_user)
):
    predictions = PredictSchoolsWithinRadius(
        location.prelim_score,
        location.latitude,
        location.longitude,
        location.radius,
        location.year
    )
    
    formatted_predictions = []
    for pred in predictions:
        d = {
            "Year": pred[0],
            "Kommun": pred[1],
            "Name": pred[2],
            "Organisitionsform": pred[3],
            "Studievagskod": pred[4],
            "Studievag": pred[5],
            "Antagningsgrans_prelim": pred[6],
            "Antagningsgrans_final": pred[7],
            "Median_prelim": pred[8],
            "Median_final": pred[9],
            "Antal_platser_prelim": pred[10],
            "Antal_platser_final": pred[11],
            "Antagna_prelim": pred[12],
            "Antagna_final": pred[13],
            "Reserver_prelim": pred[14],
            "Reserver_final": pred[15],
            "Lediga_platser_prelim": pred[16],
            "Lediga_platser_final": pred[17],
            "grans_diff": pred[18],
            "median_diff": pred[19],
            "latitude": pred[20],
            "longitude": pred[21],
            "distance": round(pred[22], 1)
        }
        formatted_predictions.append(d)
    
    return formatted_predictions 