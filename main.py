from flask import Flask, request, abort, render_template, flash, url_for, redirect,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
import configparser
from pymongo import MongoClient
import uuid
from uuid import UUID
from bson.binary import Binary, UUID_SUBTYPE, UUIDLegacy

# config initialize
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config.get('flask', 'secret_key')  # set the secret key

# define the default users account and passwords
USERS = []

client = MongoClient('mongodb://COEN6313:admin@35.183.26.186:27017/admin')
db = client.users
db_jobs = client.jobs

# This object is used to hold the settings used for logging in and initiate it.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login!'


def get_user(username):
    for user in USERS:
        if user.get("username") == username:
            return user
    return None


class User(UserMixin):
    def __init__(self, user):
        self.username = user.get("username")
        self.id = user.get("uuid")

    def get_id(self):
        return self.id

    def get_name(self):
        return self.username

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        for user in USERS:
            if user.get('uuid') == user_id:
                return User(user)
        return None



# This sets the callback for reloading a user from the session.
# The function you set should take a user ID (a unicode) and return a user object,
# or None if the user does not exist.
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.request_loader
def request_loader(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')
    if token is not None:
        username, id = token.split(":")  # naive token
        user = {
            "name": username,
            "uuid": id
        }
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user)
            return user
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        log_user = db.users.find_one({"username": username})
        if log_user and bcrypt.hashpw(request.form['password'].encode('utf-8'), log_user['password']) == log_user['password']:
            user = {
                "name": username,
                "uuid": log_user['uuid']
            }
            USERS.append(user)
            user = User(user)
            login_user(user)
            return render_template('home.html')
        else:
            flash('Invalid login, Please check your account and password!')
            return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = db.users.find_one({'username': request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            uid = uuid.uuid1()
            db.users.insert_one({'username': request.form['username'], 'password': hashpass, "uuid": uid})
            user = {
                "name": request.form['username'],
                "uuid": uid
            }
            USERS.append(user)
            user = User(user)
            login_user(user)
            return render_template('home.html')
        else:
            flash('That username already exists! Please try another name')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('See you again!')
    return render_template('login.html')


@app.route("/postjob", methods=['GET', 'POST'])
@login_required
def post_job():
    uid = current_user.get_id()
    if request.method == 'POST':
        db_jobs.jobs.insert({"email": request.form['email'], "phoneNumber": request.form['phoneNumber'], "address": request.form['address'],
                        "city": request.form['city'], "postalCode": request.form['postalCode'], "jobTitle": request.form['jobTitle'], "category": request.form['category'],
                        "date": request.form['date'], "time": request.form['time'], "jobDescription": request.form['jobDescription'], "salary": request.form['salary'],
                        "employerUid":uid, "employeeUid":None})

        return render_template('home.html')

    return render_template("postjob.html")

@app.route("/find_job",methods=['GET'])
@login_required
def find_job():
    uid = current_user.get_id()
    job_list=[]
    job_list = list(db_jobs.jobs.find({"employerUid":{"$ne":uid}}))
    return render_template('find_job.html',job_list=job_list)


@app.route("/modify/<jobid>",methods=['GET','POST'])
@login_required
def modify(jobid):
    print
    pass

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
