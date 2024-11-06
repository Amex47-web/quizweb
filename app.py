from flask import Flask, render_template, request, session
import requests
import random
import yagmail

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

API_URL = "https://opentdb.com/api.php"

# Gmail credentials for sending emails
SENDER_EMAIL = 'mail.vruttant@gmail.com'
SENDER_PASSWORD = 'aaie fmmo mjja quet'

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the quiz
@app.route('/quiz', methods=['POST'])
def quiz():
    session['user_email'] = request.form.get('email')
    category = request.form.get('category')
    difficulty = request.form.get('difficulty')
    amount = int(request.form.get('amount', 10))  # Default to 10 questions

    # Request parameters for the API
    params = {
        'amount': amount,
        'category': category,
        'difficulty': difficulty,
        'type': 'multiple'
    }

    response = requests.get(API_URL, params=params)
    questions_data = response.json().get('results')

    # Store questions and correct answers in the session
    session['questions'] = []
    session['correct_answers'] = []

    for question in questions_data:
        q = {
            'question': question['question'],
            'options': question['incorrect_answers'] + [question['correct_answer']]
        }
        random.shuffle(q['options'])  # Shuffle the answer choices
        session['questions'].append(q)
        session['correct_answers'].append(question['correct_answer'])

    return render_template('quiz.html', questions=session['questions'])

# Route to submit answers and display the result
@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form.to_dict()
    correct_answers = session.get('correct_answers')
    score = 0
    questions = session.get('questions')
    user_email = session.get('user_email')

    # Calculate the score and store user answers
    user_results = []
    for i, correct_answer in enumerate(correct_answers):
        user_answer = user_answers.get(f'question-{i}')
        if user_answer == correct_answer:
            score += 1
        user_results.append({
            'question': questions[i]['question'],
            'correct_answer': correct_answer,
            'user_answer': user_answer
        })

    # Send results via email
    send_email(user_email, score, len(correct_answers), user_results)

    return render_template('result.html', score=score, total=len(correct_answers))

def send_email(to_email, score, total, user_results):
    # Initialize yagmail with your Gmail credentials
    yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)

    # Prepare the email content
    subject = "Your Quiz Results"
    content = [
        f"Congratulations! You scored {score}/{total}.\n",
        "Here are the questions and your answers:\n\n"
    ]

    # Add each question, user's answer, and correct answer to the email content
    for result in user_results:
        content.append(f"Q: {result['question']}\n")
        content.append(f"Your Answer: {result['user_answer']}\n")
        content.append(f"Correct Answer: {result['correct_answer']}\n")
        content.append("\n")

    # Send the email
    yag.send(to=to_email, subject=subject, contents=content)

if __name__ == '__main__':
    app.run(debug=True)
