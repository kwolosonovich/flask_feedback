from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, ChirpForm
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

    if 'current_user' in session and 'current_user' == User.query.get('current_user'):
        return redirect(f"/users/{session['current_user']}")

    else:
        return render_template("homepage.html")


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

    if 'current_user' in session and 'current_user' == User.query.get('current_user'):
        return redirect(f"/users/{session['current_user']}")

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


@app.route("/users/<username>")
def user_content(username):
    '''Render content for current user'''

    if "current_user" not in session or username != session['current_user']:

        return redirect('/login')

    try:
        user = User.query.get(username)
        return render_template('content.html', user=user)

    except KeyError as e:
        print('KeyError')
        return redirect('/login')

    except TypeError as e:
        print('TypeError')
        print(username)
        return redirect('/login')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    '''Render user logout form and remove user from session.'''

    if request.method == 'POST':
        session.pop("current_user")
        return redirect("/")

    else:
        return render_template("logout.html")


@app.route("/users/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    '''Delete user and user feedback from dataase and session'''

    user = User.query.get(username)

    if "current_user" not in session or username != session['current_user']:
        return redirect("/")

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect('/')

    keyword = "Delete Account?"
    route = f"/users/{ username }/delete"
    return render_template('delete.html', keyword=keyword, route=route)


@app.route("/users/<username>/chirp/add", methods=['GET', 'POST'])
def add_chrip(username):
    '''Render new chirp form and create new chirp'''

    form = ChirpForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title,
                            content=content,
                            username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    print('invalid or GET')
    print(form)
    return render_template("chirp-form.html", username=username, form=form)


@app.route("/chirp/<feedback_id>/update", methods=['GET', 'POST'])
def edit_chirp(feedback_id):
    '''Render edit form and save changes on POST request.'''

    feedback = Feedback.query.get(feedback_id)

    if "current_user" not in session or feedback.username != session['current_user']:
        return redirect("/login")

    form = ChirpForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{session['current_user']}")

    return render_template("update.html", form=form, feedback=feedback)


@app.route("/chirp/<feedback_id>/delete", methods=["GET", "POST"])
def delete_chirp(feedback_id):
    '''Delete chirp from page and database.'''

    feedback = Feedback.query.get(feedback_id)

    print(feedback)
    print(session)
    if "current_user" not in session:
        return redirect("/")

    if request.method == 'POST':
        db.session.delete(feedback)
        db.session.commit()

        user = User.query.get(session["current_user"])

        return render_template("content.html", user=user)

    keyword = "Delete Chirp?"
    route = f"/chirp/{ feedback_id }/delete"
    return render_template('delete.html', keyword=keyword, route=route)


app.run(debug=True)