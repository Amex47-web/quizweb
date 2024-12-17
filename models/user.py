from database import users_collection  # Assuming users_collection is defined in database.py
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_email, user_name=None, password_hash=None):
        self.user_email = user_email
        self.user_name = user_name
        self.password_hash = password_hash  # Store hashed password
        self.quiz_results = []  # Initialize with an empty list, can be modified later

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def save(self):
        try:
            users_collection.update_one(
                {'user_email': self.user_email},
                {'$set': self.to_dict()},
                upsert=True
            )
        except Exception as e:
            print(f"Error saving user {self.user_email}: {e}")

    def to_dict(self):
        return {
            'user_email': self.user_email,
            'user_name': self.user_name,
            'password_hash': self.password_hash,
            'quiz_results': self.quiz_results
        }

    @classmethod
    def get_by_email(cls, user_email):
        try:
            user_data = users_collection.find_one({'user_email': user_email})
            if user_data:
                user = cls(
                    user_email=user_data['user_email'],
                    user_name=user_data.get('user_name'),
                    password_hash=user_data.get('password_hash')
                )
                user.quiz_results = user_data.get('quiz_results', [])
                return user
        except Exception as e:
            print(f"Error retrieving user {user_email}: {e}")
        return None