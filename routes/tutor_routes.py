from flask import Blueprint, request, jsonify
from bson import ObjectId
from extensions import mongo
from datetime import datetime
from services.tutor_service import TutorService

tutor_bp = Blueprint('tutor_bp', __name__)
tutor_service = TutorService()  # Initialize the service

@tutor_bp.route('/sessions', methods=['GET'])
def get_sessions():
    tutor_id = request.args.get('tutor_id')
    student_id = request.args.get('student_id')
    
    query = {}
    if tutor_id:
        query['tutor_id'] = tutor_id
    if student_id:
        query['student_id'] = student_id
        
    sessions = list(mongo.db.tutoring_sessions.find(query))
    for session in sessions:
        session['_id'] = str(session['_id'])
    
    return jsonify(sessions), 200

@tutor_bp.route('/sessions', methods=['POST'])
def create_session():
    data = request.get_json()
    
    session = {
        'tutor_id': data['tutor_id'],
        'student_id': data['student_id'],
        'course_id': data.get('course_id'),
        'scheduled_time': data['scheduled_time'],
        'duration': data['duration'],
        'status': 'scheduled',
        'created_at': datetime.utcnow()
    }
    
    result = mongo.db.tutoring_sessions.insert_one(session)
    session['_id'] = str(result.inserted_id)
    
    return jsonify(session), 201

@tutor_bp.route('/sessions/<session_id>', methods=['PUT'])
def update_session(session_id):
    data = request.get_json()
    
    # Update session
    mongo.db.tutoring_sessions.update_one(
        {'_id': ObjectId(session_id)},
        {'$set': {
            'status': data.get('status'),
            'notes': data.get('notes'),
            'updated_at': datetime.utcnow()
        }}
    )
    
    return jsonify({'message': 'Session updated successfully'}), 200

@tutor_bp.route('/availability', methods=['POST'])
def set_availability():
    data = request.get_json()
    tutor_id = data['tutor_id']
    
    availability = {
        'tutor_id': tutor_id,
        'schedule': data['schedule'],
        'updated_at': datetime.utcnow()
    }
    
    # Update or insert availability
    mongo.db.tutor_availability.update_one(
        {'tutor_id': tutor_id},
        {'$set': availability},
        upsert=True
    )
    
    return jsonify({'message': 'Availability updated successfully'}), 200

@tutor_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        user_id = data.get('user_id', 'test-user')
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"Processing message: {message}")
        
        # Get AI response using the properly initialized tutor_service
        response = tutor_service.generate_response(message)
        
        # Store chat history
        try:
            chat_entry = {
                'user_id': user_id,
                'message': message,
                'response': response,
                'timestamp': datetime.utcnow()
            }
            mongo.db.chat_history.insert_one(chat_entry)
        except Exception as e:
            print(f"Warning: Could not save chat history: {e}")
            # Continue even if saving to database fails
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow()
        }), 200
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tutor_bp.route('/history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    try:
        history = list(mongo.db.chat_history.find(
            {'user_id': user_id},
            {'_id': 0}
        ).sort('timestamp', -1).limit(50))
        
        return jsonify(history), 200
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return jsonify({'error': str(e)}), 500 