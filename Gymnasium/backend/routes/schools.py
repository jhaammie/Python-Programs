from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from hoohoohee import GetSchoolHistoricalData, GetSchoolLocation, GetGymnasiumWithinRadius, GetDataForSchools, PredictSchoolsWithinRadius
from .auth import get_current_user
import numpy as np
from sklearn.linear_model import LinearRegression

router = APIRouter()

class SchoolBase(BaseModel):
    Year: int
    Kommun: str
    Name: str
    Organisitionsform: Optional[str] = None
    Studievagskod: str
    Studievag: str
    Antagningsgrans_prelim: Optional[float] = None
    Antagningsgrans_final: Optional[float] = None
    Median_prelim: Optional[float] = None
    Median_final: Optional[float] = None
    Antal_platser_prelim: Optional[int] = None
    Antal_platser_final: Optional[int] = None
    Antagna_prelim: Optional[int] = None
    Antagna_final: Optional[int] = None
    Reserver_prelim: Optional[int] = None
    Reserver_final: Optional[int] = None
    Lediga_platser_prelim: Optional[int] = None
    Lediga_platser_final: Optional[int] = None
    grans_diff: Optional[float] = None
    median_diff: Optional[float] = None

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
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    minpreMerit: Optional[float] = None
    maxpreMerit: Optional[float] = None
    minfinMerit: Optional[float] = None
    maxfinMerit: Optional[float] = None
    programs: Optional[List[str]] = None
    page: Optional[int] = 0
    pageSize: Optional[int] = 50

class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    radius: int = Field(ge=1, le=20)
    prelim_score: float

@router.get("/schools/{school_name}", response_model=SchoolDetails)
async def get_school_details(school_name: str):
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

@router.post("/gymnasium-within-radius", response_model=PaginatedResponse)
async def get_nearby_schools(location: LocationRequest):
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

@router.post("/schools/predictions/regression", response_model=List[SchoolPrediction])
async def get_regression_predictions(location: PredictionRequest):
    # First get schools within radius
    schools, _ = GetGymnasiumWithinRadius(
        location.latitude,
        location.longitude,
        location.radius,
        0,  # page
        1000  # large page size to get all schools
    )
    
    predictions = []
    for school in schools:
        school_name = school[0]
        # Get historical data for this specific school
        historical_data = GetSchoolHistoricalData(school_name)
        
        if len(historical_data) > 1:  # Need at least 2 points for regression
            # Extract prelim and final scores
            prelim_scores = [row[6] for row in historical_data]  # Antagningsgrans_prelim
            final_scores = [row[7] for row in historical_data]   # Antagningsgrans_final
            
            # Fit regression model
            X = np.array(prelim_scores).reshape(-1, 1)
            y = np.array(final_scores)
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict final score
            predicted_final = model.predict([[location.prelim_score]])[0]
            
            # Get school location
            school_location = GetSchoolLocation(school_name)
            if school_location:
                predictions.append({
                    "Year": historical_data[0][0],  # Use most recent year
                    "Kommun": historical_data[0][1],
                    "Name": school_name,
                    "Organisitionsform": historical_data[0][3],
                    "Studievagskod": historical_data[0][4],
                    "Studievag": historical_data[0][5],
                    "Antagningsgrans_prelim": location.prelim_score,
                    "Antagningsgrans_final": predicted_final,
                    "Median_prelim": historical_data[0][8],
                    "Median_final": historical_data[0][9],
                    "Antal_platser_prelim": historical_data[0][10],
                    "Antal_platser_final": historical_data[0][11],
                    "Antagna_prelim": historical_data[0][12],
                    "Antagna_final": historical_data[0][13],
                    "Reserver_prelim": historical_data[0][14],
                    "Reserver_final": historical_data[0][15],
                    "Lediga_platser_prelim": historical_data[0][16],
                    "Lediga_platser_final": historical_data[0][17],
                    "grans_diff": predicted_final - location.prelim_score,
                    "median_diff": historical_data[0][19],
                    "latitude": school_location[0],
                    "longitude": school_location[1],
                    "distance": round(school[1], 1)  # Distance is already calculated by GetGymnasiumWithinRadius
                })
    
    # Sort by distance
    predictions.sort(key=lambda x: x["distance"])
    return predictions