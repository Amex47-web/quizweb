from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
import random
import yagmail

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_URL = "https://opentdb.com/api.php"

SENDER_EMAIL = 'mail.vruttant@gmail.com'
SENDER_PASSWORD = 'aaie fmmo mjja quet'  # Remember to use a secure method for sensitive info

# Home route for selecting quiz options
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
            flash("No questions found for the selected options.")
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
        return redirect(url_for('index'))

# Route to submit answers and show the result
@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form.to_dict()  # Collect the answers
    correct_answers = session.get('correct_answers')  # Retrieve correct answers from session  
    print(f"users answers {user_answers} and correct answers {correct_answers}")
    score = 0

    # Calculate the score
    for i, ans in enumerate(correct_answers,start=1):
        print(f"index is {i}")
        question_answer = user_answers.get(f'question-{i}')
        print(f"this is questions correct answer of user {question_answer} and official is {ans}")
        # print(f"this is correct answers {correct_answers}")
        if question_answer == ans:
            score += 1
            print(f"your score till this question{i} is = {score}")


    # Send email with results
    send_email(session['user_email'], score, len(correct_answers), session['questions'], correct_answers)

    return render_template('result.html', score=score, total=len(correct_answers))

def send_email(to_email, score, total, questions, correct_answers):
    yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
    content = [
        f"Score: {score}/{total}\n",
        "\n".join([f"Q: {questions[i]['question']}\nCorrect Answer: {correct_answers[i]}" for i in range(total)])
    ]
    yag.send(to=to_email, subject="Your Quiz Results", contents=content)

if __name__ == '__main__':
    app.run(debug=True)
