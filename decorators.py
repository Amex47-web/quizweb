from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_email = session.get('user_email')
        print(f"Decorator check: user_email={user_email}, session={session}")

        if not user_email:
            print("Unauthorized access detected.")
            # Return an error response indicating the user is not logged in
            return jsonify({"error": "login_required", "message": "Please log in to access this page."}), 401
        
        print("User is authorized.")
        return f(*args, **kwargs)

    return decorated_function
