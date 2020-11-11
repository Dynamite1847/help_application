from flask import Flask, request, abort, render_template, flash, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import configparser

# config initialize
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config.get('flask', 'secret_key') # set the secret key

# define the default users account and passwords
users = {'Yudong': {'password': 'handsome'}}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login'


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    user.is_authenticated = request.form['password'] == users[username]['password']

    return user

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    username = request.form['username']

    if (username in users) and (request.form['password'] == users[username]['password']):
        user = User()
        user.id = username
        login_user(user)
        flash(f'{username}！Welcome Login！')
        return render_template('home.html')
        # return redirect(url_for('from_start'))

    flash('Invalid login, Please check your account and password!')
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/logout')
def logout():
    username = current_user.get_id()
    logout_user()
    flash(f'{username}！See you again!')
    return render_template('login.html')

@app.route("/from_start")
@login_required
def from_start():
    return render_template("from_start.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
