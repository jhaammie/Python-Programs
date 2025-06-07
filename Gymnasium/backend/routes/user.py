from flask import Blueprint, request, jsonify
from hoohoohee import SaveUserData, GetUserData
from .auth import verify_token

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/user-data', methods=['GET'])
def get_user_data():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No authorization header"}), 401
        
    user_id = verify_token(auth_header)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
        
    user_data = GetUserData(user_id)
    if not user_data:
        return jsonify({"error": "User data not found"}), 404
        
    return jsonify({
        "email": user_data[1],
        "saved_schools": user_data[3] if user_data[3] else []
    })

@user_bp.route('/api/user-data', methods=['POST'])
def save_user_data():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No authorization header"}), 401
        
    user_id = verify_token(auth_header)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
        
    content = request.json
    saved_schools = content.get('saved_schools', [])
    
    SaveUserData(user_id, saved_schools)
    
    return jsonify({
        "message": "User data saved successfully"
    }) 