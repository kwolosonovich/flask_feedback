from app import db
from models import User, Feedback
from flask_bcrypt import Bcrypt
from lorem.text import TextLorem


def seed_database():
    print('seeding db')
    bcrypt = Bcrypt()
    title_lorem = TextLorem(wsep=" ", srange=(2, 10))
    content_lorem = TextLorem(wsep=" ", srange=(10, 20))
    # current user in database
    password = b'ava_utf8'
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    ava = User(username='ava',
           password=hashed_password,
           email='ava@gmail.com',
           first_name='Ava',
           last_name='Ava',
           profile_photo='https://images.unsplash.com/photo-1521191809347-74bcae21439c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60')
    
    print('adding user')
    db.session.add(ava)
    db.session.commit()
    
    # seed chirps
    chirps = []
    for _ in range(6):
       chirp = Feedback(title=title_lorem.sentence(),
                            content=content_lorem.paragraph(),
                            username='ava')
       chirps.append(chirp)
    
    # add list of chirps to psql  
    print('adding chirps')    
    db.session.bulk_save_objects(chirps)
    db.session.commit()

    print('chirps added')