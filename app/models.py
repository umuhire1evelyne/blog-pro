from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from datetime import timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quotes:
    '''
    Quotes class to define Quote Objects
    '''

    def __init__(self,id,author,quote,permalink):
        self.id =id
        self.author = author
        self.quote = quote
        self.permalink = "http://quotes.stormconsultancy.co.uk/quotes/31"
   

class User(UserMixin,db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    post = db.relationship('Post', backref='user', lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
   
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.username}'


class Post(db.Model):
    __tablename__= 'posts'
    id = db.Column(db.Integer,primary_key= True)
    # title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(255),nullable=False)
    category = db.Column(db.String(255),nullable=False)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref = 'post', lazy = 'dynamic')


    @classmethod
    def get_posts(cls, id):
        posts = Post.query.order_by(post_id=id).desc().all()
        return posts
    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Post {self.description}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(255),nullable=False)
    content = db.Column(db.String(1000) )
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))