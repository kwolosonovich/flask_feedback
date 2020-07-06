from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''Flutter user.'''

    default_image_url = "https://image.flaticon.com/icons/svg/184/184970.svg"

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False,
                         unique=True)
    password = db.Column(db.String,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                           nullable=False)
    profile_photo = db.Column(db.String,
                              nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")


    @classmethod
    def create_account(cls, username, password, email, first_name, last_name, profile_photo):
        '''Create new user account.'''

        hashed = bcrypt.generate_password_hash(password)
        password = hashed.decode('utf8')
        new_user = cls(username=username,
                       password=password,
                       email=email,
                       first_name=first_name,
                       last_name=last_name,
                       profile_photo=profile_photo)

        return new_user

    @classmethod
    def verify_login(cls, username, password):
        '''Verify a returning user's username and password.'''

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return True
        else:
            return False

    @classmethod
    def user_info(clsc, username):
        user = User.query.filter_by(username=username)
        return user

class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    username = db.Column(db.String,
                         db.ForeignKey('users.username'),
                         nullable=False)

    @classmethod
    def user_feedback(cls, username):
        feedback = Feedback.query.filter_by(username=username)
        return feedback
