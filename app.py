from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flutter"


connect_db(app)
db.drop_all()
db.create_all()

@app.route("/")
def welcome_page():
    '''Render welcome page.'''

    if 'current_user' not in session:
        return render_template("homepage.html")

    elif 'current_user' in session:
        return redirect(f"/users/{session['current_user']}")

@app.route("/users/<username>")
def user_content(username):
    '''Render content for current user'''

    if "current_user" not in session or username != session['current_user']:
        flash("Page not found")
        return redirect('/')

    else:
        try:
            if username == session['current_user']:
                print(username)
                print(session['current_user'])
                print('valid')
                return render_template('content.html')
        except KeyError as e:
            print('KeyError')
            # return redirect(f"/users/{session['current_user']}")

        except TypeError as e:
            print('TypeError')
            # return redirect(f"/users/{session['current_user']}")



@app.route("/register", methods=["POST", "GET"])
def register():
    '''Render register form and create new user.'''

    form = RegisterForm()

    # handle integrity error

    if form.validate_on_submit():
        print('form validated')
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

        return redirect(f"/users/{new_user.username}")
    else:
        print('form invalidated')
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Render login form and login returning user.'''

    print('login called')
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        verify_user = User.verify_login(username, password)
        if verify_user == True:
            session["current_user"] = username
            return redirect(f'/users/{username}')
        elif verify_user == False:
            flash('Please enter a valid username and password.')
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    '''Render user logout form and remove user from session.'''

    if request.method == 'POST':
        session.pop("current_user")
        return redirect("/")

    else:
        return render_template("logout.html")