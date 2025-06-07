from flask import Flask, request, jsonify
from flask_cors import CORS
from hoohoohee import GetNearestSchools, GetDataForSchools, GetGymnasiumWithinRadius, GetSchoolHistoricalData, GetSchoolLocation, PredictSchools, PredictSchoolsWithinRadius, CreateUser, GetUserByEmail, SaveUserData, GetUserData
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
import yaml
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)  # Creates an instance of app
CORS(app)

# Load JWT secret from config.yml
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
JWT_SECRET = config.get('JWT_SECRET', 'your-secret-key')
JWT_EXPIRATION_DAYS = config.get('JWT_EXPIRATION_DAYS', 1)
JWT_EXPIRATION = timedelta(days=JWT_EXPIRATION_DAYS)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + JWT_EXPIRATION
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

@app.route('/api/health-check', methods=["GET"])
def HealthCheck():
    return "OK"

@app.route('/api/gymnasium', methods=["POST"])
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

@app.route('/api/gymnasium-within-radius', methods=["POST"])
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
    page = content.get("page", 0)  # Default to page 0
    page_size = content.get("pageSize", 50)  # Default to 50 items per page
    
    lst = []
    schools, total_count = GetGymnasiumWithinRadius(a, b, radius, page, page_size)
    for school in schools:
        lst.append(school[0])
    DataList = GetDataForSchools(lst, sortby, sortOrder, minpreMerit, minfinMerit, maxpreMerit, maxfinMerit, programs, year)

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
    
    return {
        "data": list,
        "total": total_count,
        "page": page,
        "pageSize": page_size,
        "totalPages": (total_count + page_size - 1) // page_size
    }

@app.route('/api/school-details/<school_name>', methods=["GET"])
def GetSchoolDetails(school_name):
    historical_data = GetSchoolHistoricalData(school_name)
    location = GetSchoolLocation(school_name)
    
    # Format historical data
    formatted_data = []
    for row in historical_data:
        d = {
            "year": row[0],
            "program": row[1],
            "prelim_merit": row[2],
            "final_merit": row[3],
            "prelim_median": row[4],
            "final_median": row[5],
            "prelim_places": row[6],
            "final_places": row[7],
            "prelim_accepted": row[8],
            "final_accepted": row[9],
            "prelim_reserves": row[10],
            "final_reserves": row[11],
            "prelim_available": row[12],
            "final_available": row[13],
            "organization": row[14],
            "municipality": row[15]
        }
        formatted_data.append(d)
    
    return {
        "historical_data": formatted_data,
        "location": {
            "latitude": location[0] if location else None,
            "longitude": location[1] if location else None
        }
    }

@app.route('/api/predict-schools', methods=["POST"])
def PredictSchoolsEndpoint():
    content = request.json
    prelim_score = content.get("prelimScore")
    year = content.get("year")
    
    if not prelim_score:
        return {"error": "Preliminary score is required"}, 400
        
    predictions = PredictSchools(prelim_score, year)
    
    formatted_predictions = []
    for pred in predictions:
        d = {
            "school": pred[0],
            "program": pred[1],
            "prelim_merit": pred[2],
            "final_merit": pred[3],
            "prelim_median": pred[4],
            "final_median": pred[5],
            "prelim_places": pred[6],
            "final_places": pred[7],
            "prelim_accepted": pred[8],
            "final_accepted": pred[9],
            "prelim_reserves": pred[10],
            "final_reserves": pred[11],
            "prelim_available": pred[12],
            "final_available": pred[13],
            "organization": pred[14],
            "municipality": pred[15]
        }
        formatted_predictions.append(d)
    
    return {
        "predictions": formatted_predictions,
        "count": len(formatted_predictions)
    }

@app.route('/api/predict-schools-within-radius', methods=["POST"])
def PredictSchoolsWithinRadiusEndpoint():
    content = request.json
    prelim_score = content.get("prelimScore")
    latitude = content.get("latitude")
    longitude = content.get("longitude")
    radius = content.get("radius")
    year = content.get("year")
    
    if not all([prelim_score, latitude, longitude, radius]):
        return {"error": "Preliminary score, location, and radius are required"}, 400
        
    predictions = PredictSchoolsWithinRadius(prelim_score, latitude, longitude, radius, year)
    
    formatted_predictions = []
    for pred in predictions:
        d = {
            "school": pred[0],
            "program": pred[1],
            "prelim_merit": pred[2],
            "final_merit": pred[3],
            "prelim_median": pred[4],
            "final_median": pred[5],
            "prelim_places": pred[6],
            "final_places": pred[7],
            "prelim_accepted": pred[8],
            "final_accepted": pred[9],
            "prelim_reserves": pred[10],
            "final_reserves": pred[11],
            "prelim_available": pred[12],
            "final_available": pred[13],
            "organization": pred[14],
            "municipality": pred[15],
            "latitude": pred[16],
            "longitude": pred[17],
            "distance": round(pred[18], 1)
        }
        formatted_predictions.append(d)
    
    return {
        "predictions": formatted_predictions,
        "count": len(formatted_predictions)
    }

@app.route('/api/register', methods=['POST'])
def register():
    content = request.json
    email = content.get('email')
    password = content.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Check if user already exists
    existing_user = GetUserByEmail(email)
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user_id = CreateUser(email, password_hash.decode('utf-8'))
    if not user_id:
        return jsonify({'error': 'Failed to create user'}), 500
    
    # Generate token
    token = generate_token(user_id)
    
    return jsonify({
        'token': token,
        'user_id': user_id
    })

@app.route('/api/login', methods=['POST'])
def login():
    content = request.json
    email = content.get('email')
    password = content.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Get user
    user = GetUserByEmail(email)
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate token
    token = generate_token(user[0])
    
    return jsonify({
        'token': token,
        'user_id': user[0]
    })

@app.route('/api/user-data', methods=['GET'])
def get_user_data():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    data = GetUserData(user_id)
    if not data:
        return jsonify({
            'prelim_score': None,
            'favorite_schools': []
        })
    
    return jsonify({
        'prelim_score': data[0],
        'favorite_schools': data[1] if data[1] else []
    })

@app.route('/api/user-data', methods=['POST'])
def save_user_data():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    content = request.json
    prelim_score = content.get('prelim_score')
    favorite_schools = content.get('favorite_schools', [])
    
    if SaveUserData(user_id, prelim_score, favorite_schools):
        return jsonify({'message': 'Data saved successfully'})
    else:
        return jsonify({'error': 'Failed to save data'}), 500

asgi_app = WsgiToAsgi(app)

