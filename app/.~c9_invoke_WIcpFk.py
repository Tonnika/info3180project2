import os,DateTime,jwt
from app import app,db,login_manager
from flask import render_template, request,redirect, url_for, flash, jsonify
from flask_login import login_user,logout_user,current_user,login_required
from app.model import *
from werkzeug.security import check_password_hash 
from werkzeug.utils import secure_filename
from forms import *
import jwt
from functools import wraps

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

def token_authenticate(t):
    @wraps(t)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        
        if not auth:
            return jsonify({'error': 'Access Denied'}),401
        else:
            try:
                userdata = jwt.decode(auth.split(" ")[1], app.config['SECRET_KEY'])
                currentUser = UserProfile.query.filter_by(username=userdata['user']).first()
                
                if currentUser is None:
                    return jsonify({'error': 'Access Denied'}), 401
            except jwt.exceptions.InvalidSignatureError as e:
                print e
                return jsonify({'error':'Invalid Token'})
            except jwt.exceptions.DecodeError as e:
                print e 
                return jsonify({'error': 'Invalid Token'})
            return t(*args, **kwargs)
    return decorated

@app.route("/api/users/register", methods=["POST"])
def register():
    form=RegisterForm()
    if request.method and form.validate_on_submit():
        id=random.randint(1000,50000)
        username=form.username.data
        password=form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        email=form.email.data
        location=form.location.data
        biography=form.biography.data
        profile_photo=form.profile_photo.data
        joined_on=time.strftime(%d %B %Y)
        
        filename=secure_filename(profile_photo.filename)
        profile_photo.save(app.config['UPLOAD_FOLDER']+filename)
        
        profile=UserProfile(id=id,username=username,password=password,first_name=first_name,last_name=last_name,email=email,location=location,biography=biography,profile_photo=profile_photo,joined_on=joined_on)
        db.session.add(profile)
        db.session.commit()
        flash('Profile created successfully')
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route("/api/auth/login", methods=["POST"])
def login():
    form=LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        profile=UserProfile.query.filter_by(username=username,password=password).first()
        
        if profile != None and check_password_hash(profile.password, password):
            token= {

@app.route("/api/auth/logout", methods=["GET"])
def logout():
    logout_user()
    flash('Logout successful')
    return redirect(url_for('login'))

@app.route("/api/users/<int:user_id>/posts", methods=["POST"])
def posts(user_id):
    if request.method =="POST":
        form=PostForm()
        if form.validate_on_submit():
            user_id=form.user_id.data
            photo=form.photo.data
            caption=form.caption.data
            
            user=UserProfile.query.filter_by(id=user_id).first()
            filename=user.username+secure_filename(photo.filename)
            joined_on=str(datetime.date.today())
            post=Post(user_id=user_id,photo=photo,caption=caption,joined_on=joined_on)
            photo.save(os.path.join("./app",app.config['POST_IMG_UPLOAD_FOLDER'],filename))
            db.session.add(post)
            db.session.commit()
            return jsonify(status=201, message="Post created successfully")
    
@app.route("/api/users/<int:user_id>/posts", methods=["GET"])
def userPost(user_id):
    user=UserProfile.query.filter_by(user_id=user_id).first()
    post=Post.query.filter_by(user_id=user_id).all()
    follower_amt=len(Follow.query.filter_by(user_id=user_id).all())
    respond={"status":ok, "post_data":{"first_name":user.first_name "lastname": user.last_name, "location": user.location, "joined_on":strf_time(user.joined_on "%B %Y"), "biography": user.biography, "postCount": len(posts), "followers": follower_amt, "profile_image": os.path.join(app.config['UPLOAD_FOLDER'],user.profile_photo), "posts":[]}}
    
    for i in post:
        postObj={"id":post_id, "user_id":post.user_id, "photo":os.path.join(app.config['UPLOAD_FOLDER'],post.photo), "caption":post.caption,"created_on":post.created_on}
        respond["post_data"]["post"].append(postObj)
    return jsonfiy(respond)
        
@app.route("/api/users/<int:user_id>/follow", method=["POST"])
def follow(user_id):
    u =request.get_json()
    f=Follow.query.filter_by(user_id=user_id).first()
    if f!= None:
        return jsonify(status = 200, message="Error")
    follow=Follow(user_id=u['user_id'], follower_id=u['follower_id'])
    db.session.add(follow)
    db.session.commit()
    
@app.route("/api/posts", method=["GET"])
def allPost:    
    post=Post.query.filter_by(user_id=user_id).all()
    postList=[]
    for postList in post:
        user=UserProfile.query.filter_by(id=post.user_id).first()
        likes_amt=len(Like.query.filter_by(post_id=post.id).all())
        p={"id":post.id, "user_id":post.user_id, "username":user.username, "profile_photo":os.path.join(app.config['UPLOAD_FOLDER'],user.profile_photo),"photo":os.path.join(app.config'[UPLOAD_FOLDER'],post.photo), "caption":post.caption,"created_on":strf_time(post.created_on, "%d %B %Y"),"likes":likes_amt }
        postList.append(p)
    return jsonify(postList=postList)
        

@app.route("/api/posts/<int:post_id>/like", method=["POST"])     
def like(post_id):
    
    post=Post.query.filter_by(post_id=post_id)
    
        
def form_errors(form):
    errorArr=[]
    for field,errors in form.errors.items():
        for error in errors:
            errorArr.append(error)
    return errorArr
        
        
        
        
        
        
        
        
        
        