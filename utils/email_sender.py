import yagmail
from config import config
from flask import session


def send_email(quiz_result):
    sender_email=config.MAIL_USERNAME
    sender_password=config.MAIL_PASSWORD
    to_email=session['user_email']
    score=quiz_result['score']
    total=quiz_result['total_questions']
    questions=quiz_result['questions']
    correct_answers=quiz_result['correct_answers']
    print("this is session before sending email \n",session)
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        content = [
            f"Score: {score}/{total}\n",
            "\n".join([f"Q: {questions[i]['question']}\nCorrect Answer: {correct_answers[i]}" for i in range(total)]),
        ]
        yag.send(to=to_email, subject="Your Quiz Results", contents=content)
        print("Email sent successfully !")
        return True
    except Exception as e:
        print(f"unable to send email:{e}")
        return False



