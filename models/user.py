from datetime import datetime

class User:
    def __init__(self, username, email, password_hash, preferences=None, goals=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.preferences = preferences or {}
        self.goals = goals or []
        self.created_at = datetime.utcnow()
        self.learning_paths = []
        self.progress = {}

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'preferences': self.preferences,
            'goals': self.goals,
            'created_at': self.created_at,
            'learning_paths': self.learning_paths,
            'progress': self.progress
        } 