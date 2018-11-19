from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import md5
from time import time
import jwt
from app import create_app


class User(UserMixin, db.Model):
    '''
    UserMixin class that includes generic implementations
    that are appropriate for most user model classes
    '''
    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(130))
    pitches = db.relationship('pitches', backref='author', lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic = db.Column(db.String(255))
    pitcheses = db.relationship('pitches',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comments', backref='user', lazy="dynamic")



    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        '''
    with these two methods in place, a user object is now
    able to do secure password verification
    '''
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    '''
    The new avatar() method of the User class returns the URL of the user's avatar image,
    scaled to the requested size in pixels.For users that don't have an avatar registered, an "identicon" image will be generated
    The verify_reset_password_token() is a static method, which means that it can be invoked directly from the class
    '''
    def __repr__(self):
        return '{}'.format(self.username)
    '''
    Flask-login keeps track of the logged in
    user by storing its unique identifier in Flask's
    user session.
    '''
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user(cls,id):
        users = User.query.filter_by(User.id=id).all()
        return users
class pitches(db.Model):
    __tablename__= 'pitcheses'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    category = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @classmethod
    def retrieve_posts(cls,id):
        pitcheses = pitches.filter_by(id=id).all()
        return pitcheses
    '''
    pitches class represent the pitcheses pitchesed by
    users. Timestamp is set to default and passsed datetime.utcnow--> function.
    SQLAlchemy will set the field to the value of calling that function
    and not the result of calling it without ()
    The user_id field is initialized as a foreign key to user.id,
    which means that it references an id value from the users table
    '''

    def __repr__(self):
        return '{}'.format(self.body)


class Comments(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key= True)
    details = db.Column(db.String(255))
    pitches_id = db.Column(db.Integer,db.ForeignKey('pitcheses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
