from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Tuple
from hoohoohee import GetSchoolHistoricalData, GetSchoolLocation, GetGymnasiumWithinRadius, GetDataForSchools, PredictSchoolsWithinRadius
from .auth import get_current_user
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

router = APIRouter()

# Cache for school locations
school_location_cache: Dict[str, Tuple[float, float]] = {}

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
    radius: float
    prelim_score: float

class SchoolNameRequest(BaseModel):
    school_name: str

def get_school_location(school_name: str) -> Optional[Tuple[float, float]]:
    """Get school location from cache or database."""
    if school_name in school_location_cache:
        return school_location_cache[school_name]
    
    location = GetSchoolLocation(school_name)
    if location:
        school_location_cache[school_name] = location
    return location

@router.post("/school-details", response_model=SchoolDetails)
async def get_school_details(request: SchoolNameRequest):
    historical_data = GetSchoolHistoricalData(request.school_name)
    location = GetSchoolLocation(request.school_name)
    
    formatted_data = []
    for row in historical_data:
        d = {
            "Year": row[0],  # år
            "Kommun": row[15],  # kommun
            "Name": request.school_name,  # Use the requested school name
            "Organisitionsform": row[14],  # organistionsform
            "Studievagskod": row[16],  # studievagskod
            "Studievag": row[1],  # studieväg
            "Antagningsgrans_prelim": row[2],  # antagningsgräns_prelim
            "Antagningsgrans_final": row[3],  # antagningsgräns_final
            "Median_prelim": row[4],  # median_prelim
            "Median_final": row[5],  # median_final
            "Antal_platser_prelim": row[6],  # antal_platser_prelim
            "Antal_platser_final": row[7],  # antal_platser_final
            "Antagna_prelim": row[8],  # antagna_prelim
            "Antagna_final": row[9],  # antagna_final
            "Reserver_prelim": row[10],  # reserver_prelim
            "Reserver_final": row[11],  # reserver_final
            "Lediga_platser_prelim": row[12],  # lediga_platser_prelim
            "Lediga_platser_final": row[13],  # lediga_platser_final
            "grans_diff": row[17],  
            "median_diff": row[18]
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
            "Year": school[0],              # år
            "Studievag": school[1],         # studieväg
            "Antagningsgrans_prelim": school[2],    # antagningsgräns_prelim
            "Antagningsgrans_final": school[3],     # antagningsgräns_final
            "Median_prelim": school[4],             # median_prelim
            "Median_final": school[5],              # median_final
            "Antal_platser_prelim": school[6],      # antal_platser_prelim
            "Antal_platser_final": school[7],       # antal_platser_final
            "Antagna_prelim": school[8],            # antagna_prelim
            "Antagna_final": school[9],             # antagna_final
            "Reserver_prelim": school[10],          # reserver_prelim
            "Reserver_final": school[11],           # reserver_final
            "Lediga_platser_prelim": school[12],    # lediga_platser_prelim
            "Lediga_platser_final": school[13],     # lediga_platser_final
            "Organisitionsform": school[14],        # organistionsform
            "Kommun": school[15],                   # kommun
            "Studievagskod": school[16],            # studievägskod
            "grans_diff": school[17],               # gräns_diff
            "median_diff": school[18],              # median_diff
            "Name": school[19]                      # skola
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
            # Group data by program code
            program_data = {}
            for row in historical_data:
                if row[2] is not None and row[3] is not None:  # Check for None values in prelim and final scores
                    program_code = str(row[16])  # studievägskod
                    if program_code not in program_data:
                        program_data[program_code] = {
                            'prelim_scores': [],
                            'final_scores': [],
                            'years': []
                        }
                    program_data[program_code]['prelim_scores'].append(float(row[2]))  # antagningsgräns_prelim
                    program_data[program_code]['final_scores'].append(float(row[3]))   # antagningsgräns_final
                    program_data[program_code]['years'].append(row[0])  # år
            
            # Make predictions for each program
            for program_code, data in program_data.items():
                if len(data['prelim_scores']) > 1:  # Need at least 2 valid points for regression
                    # Create feature matrix with prelim scores
                    X = np.array(data['prelim_scores']).reshape(-1, 1)
                    y = np.array(data['final_scores'])
                    
                    # Skip if any NaN values
                    if not np.isnan(X).any() and not np.isnan(y).any():
                        model = LinearRegression()
                        model.fit(X, y)
                        
                        # Predict final score using prelim score
                        predicted_final = model.predict([[float(location.prelim_score)]])[0]
                        
                        # Calculate confidence level based on:
                        # 1. Number of data points
                        # 2. Recency of data
                        # 3. Variance in historical data
                        num_data_points = len(data['prelim_scores'])
                        max_year = max(data['years'])
                        current_year = datetime.now().year
                        year_diff = current_year - max_year
                        
                        # Calculate variance in historical data
                        prelim_variance = np.var(data['prelim_scores'])
                        final_variance = np.var(data['final_scores'])
                        
                        # Calculate confidence score (0-100)
                        data_points_score = min(100, num_data_points * 20)  # 5 points = 100% confidence
                        recency_score = max(0, 100 - (year_diff * 20))  # -20% per year
                        variance_score = max(0, 100 - (prelim_variance + final_variance) * 10)  # -10% per unit of variance
                        
                        confidence = (data_points_score + recency_score + variance_score) / 3
                        
                        # Calculate probability of getting in
                        # Based on how many historical final scores were below the predicted score
                        historical_final_scores = np.array(data['final_scores'])
                        probability = np.mean(historical_final_scores >= predicted_final) * 100
                        
                        # Get school location from cache or database
                        school_location = get_school_location(school_name)
                        if school_location:
                            # Find the most recent data for this program
                            program_rows = [row for row in historical_data if str(row[16]) == program_code]
                            if program_rows:
                                latest_data = program_rows[0]  # Most recent data for this program
                                
                                # Calculate median difference
                                median_prelim = latest_data[4]  # median_prelim
                                median_final = latest_data[5]   # median_final
                                median_diff = median_final - median_prelim if median_prelim is not None and median_final is not None else None
                                
                                predictions.append({
                                    "Year": latest_data[0],  # år
                                    "Kommun": latest_data[15],  # kommun
                                    "Name": school_name,
                                    "Organisitionsform": latest_data[14],  # organistionsform
                                    "Studievagskod": program_code,  # studievägskod
                                    "Studievag": latest_data[1],  # studieväg
                                    "Antagningsgrans_prelim": location.prelim_score,
                                    "Antagningsgrans_final": predicted_final,
                                    "Median_prelim": median_prelim,
                                    "Median_final": median_final,
                                    "Antal_platser_prelim": latest_data[6],  # antal_platser_prelim
                                    "Antal_platser_final": latest_data[7],   # antal_platser_final
                                    "Antagna_prelim": latest_data[8],        # antagna_prelim
                                    "Antagna_final": latest_data[9],         # antagna_final
                                    "Reserver_prelim": latest_data[10],      # reserver_prelim
                                    "Reserver_final": latest_data[11],       # reserver_final
                                    "Lediga_platser_prelim": latest_data[12], # lediga_platser_prelim
                                    "Lediga_platser_final": latest_data[13],  # lediga_platser_final
                                    "grans_diff": predicted_final - location.prelim_score,
                                    "median_diff": median_diff,
                                    "latitude": school_location[0],
                                    "longitude": school_location[1],
                                    "distance": round(school[1], 1),  # Distance is already calculated by GetGymnasiumWithinRadius
                                    "confidence": round(confidence, 1),  # Confidence level (0-100)
                                    "probability": round(probability, 1)  # Probability of getting in (0-100)
                                })
    
    # Sort by Antal_platser_final, Lediga_platser_final, probability, and confidence (all descending)
    predictions.sort(key=lambda x: (
        -(x["Antal_platser_final"] or 0),
        -(x["Lediga_platser_final"] or 0),
        -(x["probability"] or 0),
        -(x["confidence"] or 0)
    ))
    return predictions[:25]