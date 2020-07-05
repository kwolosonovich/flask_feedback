from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
# from models import User

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret123"

# connect_db(app)
# db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def welcome_page():
    '''Render welcome page.'''

    return render_template("homepage.html")

@app.route("/register")
def register():
    return render_template("register.html")