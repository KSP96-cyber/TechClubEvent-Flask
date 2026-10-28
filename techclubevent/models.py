from techclubevent import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to built-in attributes
# which will be able to call in our views.
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    AUTHOR = 1
    GENERAL = 2
    # 'role' is an integer, and define constants to represent each role. This approach is more efficient and less error-prone.
    role = db.Column(db.Integer, default=GENERAL)  
    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects EventPosts to a User Author.
    posts = db.relationship('EventPost', backref='post_author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"
class EventPost(db.Model):
     __tablename__ = 'event_posts'

     id = db.Column(db.Integer, primary_key=True)
     author_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     title = db.Column(db.String(140), nullable=False)
     text = db.Column(db.Text, nullable=False)
     author = db.relationship('User', backref='authored_posts')

     def __init__(self, title, text, author_id):
        self.title = title
        self.text = text
        self.author_id = author_id
     def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"

    #end
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event_posts.id'), nullable=False)
    checked_in = db.Column(db.Boolean, default=False, nullable=False)

class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event_posts.id'), nullable=False)
    checked_in = db.Column(db.Boolean, default=False, nullable=False)
    # Any additional fields related to the attendee

    # # Relationships (if not already defined in User and Event models)
    user = db.relationship('User', backref='attendees')
    event = db.relationship('EventPost', backref='attendees')
     


