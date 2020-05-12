from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_mysqldb import MySQL
#from datetime import datetime
#from flask_migrate import Migrate


app = Flask(__name__)
app.config["DEBUG"] = True

# Set up the database:
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ESIS668",
    password="python123",
    hostname="ESIS668.mysql.pythonanywhere-services.com",
    databasename="ESIS668$668gradebook",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

#app.config['MYSQL_HOST'] = 'ESIS668.mysql.pythonanywhere-services.com'
#app.config['MYSQL_USER'] = 'ESIS668'
#app.config['MYSQL_PASSWORD'] = 'python123'
#app.config['MYSQL_DB'] = 'ESIS668$668gradebook"'

#mysql = MySQL(app)



# Set up the login manager:
#app.secret_key = "umbc2020"
#login_manager = LoginManager()
#login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


# Object to hold all users
all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "bob": User("bob", generate_password_hash("less-secret")),
    "caroline": User("caroline", generate_password_hash("completely-secret")),
}

#@login_manager.user_loader
#def load_user(user_id):
    #return all_users.get(user_id)

# Gradebook table
class Gradebook(db.Model):

    __tablename__ = "gradebook"

    s_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    major = db.Column(db.String(128))
    email = db.Column(db.String(128))
    a1 = db.Column(db.Integer)  #represents each assignment's grade
    a2 = db.Column(db.Integer)
    a3 = db.Column(db.Integer)
    a4 = db.Column(db.Integer)


# ROUTES

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")

    if request.form["username"] != "admin" or request.form["password"] != "secret":
        return render_template("login_page.html")

    return redirect(url_for('gradebook'))

# Logout re-routing
@app.route("/logout/")
#@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))

# Gradebook page
@app.route('/gradebook/', methods=["GET", "POST"])
#@login_required
def gradebook():
  if request.method == "GET":
     #cur = mysql.connection.cursor()
     #cur.execute("SELECT * FROM gradebook")
     #data = cur.fetchall()
     #mysql.connection.commit()
     #cur.close()
     #return render_template("gradebook.html", data = data)
     #return render_template("main_page.html", comments=Comment.query.all())
     return render_template("gradebook.html", student=Gradebook.query.all())

# Student info page
@app.route('/student/<s_id>', methods=["GET", "POST"])
#@login_required
def load_student(s_id):
    return render_template("student_info.html")

