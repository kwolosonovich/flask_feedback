from app import db
from models import User, Feedback

def seed_database():
    db.drop_all()
    db.create_all()

    # current user in database

    ava = User(username='ava',
               password='ava',
               email='ava@gmail.com',
               first_name='ava',
               last_name='ava',
               profile_photo='https://images.unsplash.com/photo-1521191809347-74bcae21439c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
               )

    db.session.add(ava)

    chirp = Feedback(title="test title",
                     content="test content",
                     username='ava')

    db.session.add(chirp)
    db.session.commit()