from datetime import datetime
from typing import List, Dict

class LearningPath:
    def __init__(self,
                 user_id: str,
                 title: str,
                 description: str,
                 goals: List[str],
                 courses: List[Dict] = None):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.goals = goals
        self.courses = courses or []
        self.created_at = datetime.utcnow()
        self.status = "active"
        self.progress = 0.0

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'goals': self.goals,
            'courses': self.courses,
            'created_at': self.created_at,
            'status': self.status,
            'progress': self.progress
        } 