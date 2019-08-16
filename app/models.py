from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    pitch = db.relationship('Pitch', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

#tying a user i.e an admin to a drift post
    pitch=db.relationship('Pitch',backref='author',lazy='dynamic')

    #tying a user to a comment
    comments=db.relationship('Comment',backref='commenter',lazy="dynamic")

    #tying a user to a custom drift
    #customdrifts=db.relationship('CustomDrift',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure, password)
    def save_user(self):
        '''
        save instance for a user
        '''
        db.session.add(self)
        db.session.commit()  
        
    @classmethod
    def check_roles(cls,user_id,role_id):
        get_role=User.query.filter_by(id=user_id).filter_by(role_id=role_id).first()
        return get_role    
    
    def __repr__(self):
        return f'User {self.username}'  


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pitch(db.Model):
    '''
    '''
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    company = db.Column(db.String(), index = True)
    state = db.Column(db.String(), index = True)
    qualifications = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment',backref='pitch',lazy='dynamic')

    def save_pitches(self):
        '''
        Function that saves a drift post
        '''
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_pitches(cls, id):
        pitches = Pitch.query.order_by(pitch_id=id).desc().all()
        return pitches

    def __repr__(self):
        return f'Pitch {self.description}'
    @classmethod
    def get_admin_pitches(cls,user,page):
        '''
        Function that fetches all drift post for a single admin
        '''
        pitches_user=Pitch.query.filter_by(author=user).order_by(Pitch.date.desc()).paginate(page=page,per_page=5) 
        return pitches_user   

    def __repr__(self):
        return f'PitchID:{self.id}--Date{self.date}--Title{self.location}'    

    

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    def save_comment(self):
        '''
        Function that saves a new comment
        '''
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def get_comments(cls,pitch_id):
        '''
        Function that fetches a specific drift post comments
        '''
        
        comments=Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments
    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"












class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'