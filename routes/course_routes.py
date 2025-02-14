from flask import Blueprint, request, jsonify
from bson import ObjectId
from extensions import mongo

course_bp = Blueprint('courses', __name__)

@course_bp.route('/', methods=['GET'])
def get_courses():
    courses = mongo.db.courses.find()
    course_list = []
    for course in courses:
        course['_id'] = str(course['_id'])
        course_list.append(course)
    return jsonify(course_list)

@course_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    course['_id'] = str(course['_id'])
    return jsonify(course), 200

@course_bp.route('/<course_id>/progress', methods=['POST'])
def update_progress(course_id):
    data = request.get_json()
    user_id = data['user_id']
    
    progress = {
        'user_id': user_id,
        'course_id': course_id,
        'completion_status': data['completion_status'],
        'completed_modules': data.get('completed_modules', []),
        'quiz_scores': data.get('quiz_scores', {})
    }
    
    # Update or insert progress
    mongo.db.progress.update_one(
        {'user_id': user_id, 'course_id': course_id},
        {'$set': progress},
        upsert=True
    )
    
    return jsonify({'message': 'Progress updated successfully'}), 200 