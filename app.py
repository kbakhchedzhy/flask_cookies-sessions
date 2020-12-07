from flask import Flask
from flask import request, session, make_response

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

    if request.cookies.get('visited'):
        visited_counter = int(request.cookies['visited'])

    if visited_counter == 0:
        response = make_response("Пользовать " + username + " и зашел первый раз.")
    else:
        response = make_response("Пользовать " + username + " и заходил " + str(visited_counter) + " раз(a).")
    response.set_cookie('visited', str(visited_counter + 1))
    return response


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
        response = make_response("Пользовать вошел в систему как " + username)
        response.set_cookie('visited', str(0))
        return response


@app.route('/logout')
def logout():
    """
    Logout from sessions
    :return: info about logout
    """
    session.pop('username', None)
    response = make_response("Пользовать вышел из системы")
    response.set_cookie('visited', '', 0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
