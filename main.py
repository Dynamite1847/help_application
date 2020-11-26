from flask import Flask, request, abort, render_template, flash, url_for, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
import configparser
from pymongo import MongoClient
import uuid

# config initialize
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config.get('flask', 'secret_key')  # set the secret key

# define the default users account and passwords
users = {'Yudong': {'password': 'handsome'}}

# This object is used to hold the settings used for logging in and initiate it.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login!'


class User(UserMixin):
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        pass


# This sets the callback for reloading a user from the session.
# The function you set should take a user ID (a unicode) and return a user object,
# or None if the user does not exist.
@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return None
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return None
    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    username = request.form['username']
    client = MongoClient('localhost', 27017)
    db = client.users
    log_user = db.users.find_one({"username": username})
    if log_user and bcrypt.hashpw(request.form['password'].encode('utf-8'), log_user['password']) == log_user['password']:
        user = User()
        user.id = username
        login_user(user)

        return render_template('home.html')
        # return redirect(url_for('from_start'))
    else:
        flash('Invalid login, Please check your account and password!')
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        client = MongoClient('localhost', 27017)
        db = client.users
        existing_user = db.users.find_one({'username': request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            uid = uuid.uuid1()
            db.users.insert_one({'username': request.form['username'], 'password': hashpass, "uuid": uid})
            user = User()
            user.id = request.form['username']
            login_user(user)
            return render_template('home.html')

        flash('That username already exists! Please try another name')
        return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/signup")
def signup():
    return render_template("register.html")


@app.route('/logout')
def logout():
    username = current_user.get_id()
    logout_user()
    flash('See you again!')
    return render_template('login.html')


@app.route("/from_start")
@login_required
def from_start():
    return render_template("from_start.html")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
