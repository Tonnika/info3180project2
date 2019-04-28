from . import db

class Post(db.Model):
    __tablename__='Post'
    
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    photo=db.Column(db.String(255))
    caption=db.Column(db.String(255))
    created_on=db.Column(db.DateTime)
    
    def __init__(self,id,user_id,photo,caption,created_on):
        #self.id=id
        self.user_id=user_id
        self.photo=photo
        self.caption=caption
        self.created_on=created_on
    
    def is_authenticated(self):
        return True
    
    def is_actice(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Post %r>' % self.user_id
        
class UserProfile(db.Model):
    __tablename__='Users'
    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True)
    password=db.Column(db.String(255))
    first_name=db.Column(db.String(80))
    last_name=db.Column(db.String(80))
    email=db.Column(db.String(80), unique=True)
    location=db.Column(db.String(80))
    biography=db.Column(db.String(255))
    profile_photo=db.Column(db.String(255))
    joined_on=db.Column(db.DateTime)
    
    def __init__(self,id,username,password,first_name,last_name,email,location,biography,profile_photo,joined_on):
        self.id=id
        self.username=username
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.location=location
        self.biography=biography
        self.profile_photo=profile_photo
        self.joined_on=joined_on
    
    def is_authenticated(self):
        return True
    
    def is_actice(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % self.username

class Like(db.Model):
    __tablename__='Likes'
    
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, primary_key=True)
    post_id=db.Column(db.Integer, primary_key=True)
    
    def __init__(self,id,user_id,post_id):
        self.id=id
        self.user_id=user_id
        self.post_id=post_id
    
    def is_authenticated(self):
        return True
    
    def is_actice(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Like %r>' % self.post_id
    
class Follow(db.Model):
    __tablename='Follows'
        
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,primary_key=True)
    follower_id=db.Column(db.Integer,primary_key=True)
    
    def __init__(self,id,user_id,follower_id):
        self.id=id
        self.user_id=user_id
        self.follower_id=follower_id
    
    def is_authenticated(self):
        return True

    def is_actice(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Follow %r>' % self.follow_id


    
    
    
    
        
        
        
        