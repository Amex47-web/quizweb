from flask import Flask, render_template, request, session, redirect, url_for, flash,jsonify
from werkzeug.security import generate_password_hash
from google_auth import get_google_login_url, handle_google_callback
from config import config
import requests
import random
from database import db  # Importing the `db` object from `database.py`
from google_auth_oauthlib.flow import Flow
import os
from utils.email_sender import send_email
from models.user import User
from decorators import login_required
from datetime import datetime,timezone

app = Flask(__name__)
app.config.from_object(config)

app.secret_key = config.SECRET_KEY # Secret key 

API_URL = config.API_URL
SENDER_EMAIL = config.MAIL_USERNAME
SENDER_PASSWORD = config.MAIL_PASSWORD
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Home route for selecting quiz options
@app.route('/')
def home():  
    return render_template('index.html',session=session)  # Rendering login page with Tailwind CSS


# Login Route

@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Assuming the frontend sends JSON data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Query the user from the database
    user = User.get_by_email(email)
    if not user:
        return jsonify({'error': 'User does not exist. Please sign up.'}), 404

    if not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Store session data securely
    session.clear()
    session['user_email'] = user.user_email
    session['user_name'] = user.user_name

    flash("Login successful!", "success")
    return jsonify({'message': 'Login successful', 'user': user.user_name}), 200



    
@app.route('/loginwithgoogle')
def gooogle_login():
    google_login_url = get_google_login_url()
    print("google login url fetched ",google_login_url)
    return redirect(google_login_url)


@app.route('/auth/callback')
def callback():
    # Handle the Google callback and save user info to session
    handle_google_callback()
    print("Session after Google OAuth callback:", session)  # Check session content
    flash('Successfully logged in!', 'success')
    return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if user already exists in the database
    existing_user = User.get_by_email(email)
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    # Create a new user instance
    new_user = User(user_email=email, user_name=username)
    new_user.set_password(password)  # Hash and set the password
    new_user.save()  # Save the user to the database

    flash("Signup successful! Please log in.", "success")
    return jsonify({'message': 'Signup successful', 'user': username}), 201


 
# Logout Route
@app.route('/logout')
def logout():
    user_email = session.get('user_email')
    if user_email:
        print(f"Logging out user: {user_email}")
    session.clear()  # Clear the session
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))


@app.route('/quiz/live', methods=['POST'])
@login_required
def quiz():
    user_email=session['user_email']
    if not user_email:           
                return redirect(url_for('home'))
    
    category = request.form.get('category')
    difficulty = request.form.get('difficulty')
    amount = int(request.form.get('amount', 10))

    params = {
        'amount': amount,
        'category': category,
        'difficulty': difficulty,
        'type': 'multiple'
    }

    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        questions_data = response.json().get('results')
        if not questions_data:
            flash("No questions found from the server")
            return redirect(url_for('index'))

        session['questions'] = []
        session['correct_answers'] = []

        for question in questions_data:
            q = {
                'question': question['question'],
                'options': question['incorrect_answers'] + [question['correct_answer']]
            }
            random.shuffle(q['options'])
            session['questions'].append(q)
            session['correct_answers'].append(question['correct_answer'])

        return render_template('quiz.html', questions=session['questions'])
    else:
        flash("Error retrieving questions. Try again.")
        return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    user_email = session.get('user_email')
    user = User.get_by_email(user_email)

    if not user:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for('logout'))

    return render_template('profile.html', user=user)


@app.route('/quiz/result', methods=['POST'])
def quiz_result():
    user_answers = request.form.to_dict()
    correct_answers = session.get('correct_answers')
    score = 0

    # Calculate score based on correct answers
    for i, ans in enumerate(correct_answers, start=1):
        question_answer = user_answers.get(f'question-{i}')
        if question_answer == ans:
            score += 1

    user_email = session.get('user_email', None)
    user_name = session.get('user_name',None)
    quiz_result = {
        "score": score,
        "total_questions": len(correct_answers),
        "questions": session['questions'],
        "correct_answers": correct_answers,
        "created_at": datetime.now(timezone.utc),

    }

    # Send email with quiz result
    send_email(quiz_result)
    print("email sent and goin forward")

    if user_email:
        # Retrieve the user from the database, or create a new user if not found
        user = User.get_by_email(user_email)
        # print("this is user from database",user)
        if not user:
            user = User(user_email=user_email, user_name=user_name)  # Pass name to the constructor

        # Append the latest quiz result and save it using the save method in User model
        user.quiz_results.append(quiz_result)
        user.save()


    return render_template('result.html', score=score, total=len(correct_answers))

@app.route('/quiz/select')
@login_required
def quiz_select():
    return render_template('form.html')




 
if __name__ == '__main__':
    app.run(debug=True)
