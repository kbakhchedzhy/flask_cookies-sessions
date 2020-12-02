from flask import Flask, render_template, request, make_response, session

app = Flask(__name__)
app.secret_key = b'wqorfwqoir3'


@app.route('/')
def index():
    """
    Main
    :return: info about user and how much he visited page (using sessions)
    """
    visited_counter = 0

    if session.get('username'):
        username = session['username']
    else:
        username = 'Аноним'

    if session.get('visited'):
        visited_counter = session['visited']
    else:
        session['visited'] = 0

    session['visited'] += 1

    if visited_counter == 0:
        return f"Пользовать {username} и зашел первый раз(a)."

    return f"Пользовать {username} и заходил {visited_counter} раз."


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Require registration.
    :return: if user is none - input form, else - string about user
    """
    if session.get('username'):
        username = session['username']
        return f"Пользовать вошел в систему как {username}"
    elif request.method == 'GET':
        return """
                <form action = 'http://localhost:5000/login', method='POST'>
                    <input name = "username">
                    <input type = "submit">
                </form>
                """

    elif request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        session['visited'] = 0
        return f"Пользовать вошел в систему как {username}"


@app.route('/logout')
def logout():
    """
    Logout from sessions
    :return: info about logout
    """
    session.pop('username', None)
    session.pop('visited', None)
    return f"Пользовать вышел из системы"


if __name__ == '__main__':
    app.run(debug=True)
