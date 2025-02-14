from datetime import datetime
from typing import List, Dict

class Course:
    def __init__(self, 
                 title: str,
                 description: str,
                 difficulty_level: str,
                 topics: List[str],
                 duration: int,  # in minutes
                 prerequisites: List[str] = None,
                 skills_gained: List[str] = None,
                 content: Dict = None):
        self.title = title
        self.description = description
        self.difficulty_level = difficulty_level
        self.topics = topics
        self.duration = duration
        self.prerequisites = prerequisites or []
        self.skills_gained = skills_gained or []
        self.content = content or {}
        self.created_at = datetime.utcnow()
        self.rating = 0.0
        self.total_ratings = 0

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'topics': self.topics,
            'duration': self.duration,
            'prerequisites': self.prerequisites,
            'skills_gained': self.skills_gained,
            'content': self.content,
            'created_at': self.created_at,
            'rating': self.rating,
            'total_ratings': self.total_ratings
        } 