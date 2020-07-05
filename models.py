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

    __tablename__ = "users"

    default_image_url = "https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png"

    username = db.Column(db.String(20),
                   primary_key=True)
    password = db.Column(db.String,
                         default=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                           nullable=False)
    profile_photo = db.Column(db.String,
                              nullable=False,
                              default=default_image_url)
