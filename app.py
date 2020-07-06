from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flutter"


connect_db(app)
db.create_all()

@app.route("/")
def welcome_page():
    '''Render welcome page.'''

    return render_template("homepage.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    '''Render register form and create new user.'''

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        profile_photo = form.profile_photo.data

        new_user = User.create_account(username, password, email, first_name, last_name, profile_photo)

        db.session.add(new_user)
        db.session.commit()

        session["current_user"] = username

        return redirect("/")
    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Render login form and lopin returning user.'''

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        verify_user = User.verify_login(username, password)
        if verify_user == True:
            session["current_user"] = username
            return render_template("content.html", username=username)
        elif verify_user == False:
            flash('Please enter a valid username and password.')
            return render_template("login.html")
    else:
        return render_template("login.html")