from flask import Flask, session, redirect

SESSION_USER = "session.user"

app = Flask(__name__)


@app.route('/')
def hello_world():

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
