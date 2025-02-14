from datetime import datetime
from typing import Dict, Any

class Progress:
    def __init__(self,
                 user_id: str,
                 course_id: str,
                 learning_path_id: str = None):
        self.user_id = user_id
        self.course_id = course_id
        self.learning_path_id = learning_path_id
        self.started_at = datetime.utcnow()
        self.last_accessed = datetime.utcnow()
        self.completion_status = 0  # percentage
        self.completed_modules = []
        self.quiz_scores = {}
        self.time_spent = 0  # in minutes

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'course_id': self.course_id,
            'learning_path_id': self.learning_path_id,
            'started_at': self.started_at,
            'last_accessed': self.last_accessed,
            'completion_status': self.completion_status,
            'completed_modules': self.completed_modules,
            'quiz_scores': self.quiz_scores,
            'time_spent': self.time_spent
        } 