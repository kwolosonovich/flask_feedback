from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from seed import seed_database

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flutter"


connect_db(app)

db.drop_all()
db.create_all()

# seed_database()

@app.route("/")
def welcome_page():
    '''Render welcome page.'''

    if 'current_user' not in session:
        return render_template("homepage.html")

    elif 'current_user' in session:
        print(session['current_user'])
        return redirect(f"/users/{session['current_user']}")

@app.route("/users/<username>")
def user_content(username):
    '''Render content for current user'''

    if "current_user" not in session or username != session['current_user']:
        flash("Page not found")
        print('first if')
        return redirect('/logout')

    else:
        try:
            # print('in try')
            # if username == session['current_user']:
                # feedback = Feedback.user_feedback(username)
                # user = User.user_info(username)
            print(username)
            # chirps = Feedback.query.get(1)
            user = User.query.get(username)

            return render_template('content.html', user=user)

        except KeyError as e:
            print('KeyError')
            # return redirect(f"/users/{session['current_user']}")
            return redirect('/login')

        except TypeError as e:
            print('TypeError')
            print(username)
            return redirect('/login')


@app.route("/register", methods=["POST", "GET"])
def register():
    '''Render register form and create new user.'''

    form = RegisterForm()

    try:
        if form.validate_on_submit():
            print('form validated')
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            profile_photo = form.profile_photo.data
            if len(profile_photo) == 0 or profile_photo is None:
                profile_photo = User.default_image_url

            User.create_account(username=username,
                                password=password,
                                email=email,
                                first_name=first_name,
                                last_name=last_name,
                                profile_photo=profile_photo)

            db.session.commit()

            session["current_user"] = username

            return redirect(f"/users/{username}")

        else:
            print('form invalidated')
            return render_template("register.html", form=form)

    except IntegrityError as e:
        flash('Sorry that username is already taken. Please enter a new username')
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Render login form and login returning user.'''

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        verify_user = User.authenticate(username, password)
        if verify_user == True:
            session["current_user"] = username
            return redirect(f'/users/{username}')
        else:
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


@app.route("/user/<username>/delete", methods=["POST"])
def delete_user(username):
    '''Delete user and user feedback from dataase and session'''

    r = request.forms.get('first')
    form = request.forms.get()
    print(r)
    print(form)
    flash("Account Deleted")

    return render_template("logout.html")

