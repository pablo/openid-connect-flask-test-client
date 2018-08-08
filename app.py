from flask import Flask, session, redirect
from config import GOOGLE_API_KEY

SESSION_USER = "session.user"

app = Flask(__name__)


@app.route('/')
def hello_world():
    print("Using my API KEY: " + GOOGLE_API_KEY)
    return 'Hello World!'

@app.route('/secured')
def secured_resource():
    if SESSION_USER in session:
        return ''
    else:
        # redirect to login
        return redirect('http://localhost:8080/')


if __name__ == '__main__':
    app.run()
