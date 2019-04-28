import os,DateTime,jwt
from app import app,db,login_manager
from flask import render_template, request,redirect, url_for, flash, jsonify
from flask_login import login_user,logout_user,current_user,login_required
from werkzeug.security import check_password_hash 
from werkzeug.utils import secure_filename
from forms import *
from model import *
import jwt
from functools import wraps


def authenticate(token):
    @wraps(token)
    def decorated(*args, **kwargs):
        
        auth = request.headers.get('Authorization', None)
        
        if not auth:
            return jsonify({'error': 'Access Denied'}), 401
        else:
            try:
                userdata = jwt.decode(auth.split(" ")[1], app.config['SECRET_KEY'])
                currentUser = Users.query.filter_by(username = userdata['user']).first()
                
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
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/api/users/register", methods=["POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        id=random.randint(1000,50000)
        username=form.username.data
        password=form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        email=form.email.data
        location=form.location.data
        biography=form.biography.data
        profile_photo=form.profile_photo.data
        joined_on= str(datetime.date.today())
        
        filename=secure_filename(profile_photo.filename)
        profile_photo.save(app.config['UPLOAD_FOLDER']+filename)
        
        user=UserProfile(username=username,password=password,first_name=first_name,last_name=last_name,email=email,location=location,biography=biography,profile_photo=profile_photo,joined_on=joined_on)
        db.session.add(user)
        db.session.commit()
        return jsonify(message = 'Profile created')

@app.route("/api/auth/login", methods=["POST"])
def login():
    form=LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user=UserProfile.query.filter_by(username=username,password=password).first()
        
        if user != None and check_password_hash(user.password, password):
            token= {'user': user.username}
            jwt_token = jwt.encode(token, app.config['SECRET_KEY'],algorithm="HS256")
            response = {'message': 'Login Successful'}
            
            return jsonify(response)
        return jsonify(errors="Login details are incorrect")
    return jsonify(errors=form_errors(form))

@app.route("/api/auth/logout", methods=["GET"])
@token_authenticate
def logout():
    return jsonify(message="Logout successful")
    
@app.route("/api/posts", method=["GET"])
@authenticate
def allPost():    
    Epost=Post.query.all()
    postList=[]
    for post in Epost:
        user=UserProfile.query.filter_by(id=post.user_id).first()
        likes_amt=len(Like.query.filter_by(post_id=post.id).all())
        p={"id":post.id, "user_id":post.user_id, "username":user.username, "profile_photo": os.path.join(app.config['UPLOAD_FOLDER'],user.profile_photo),"photo":os.path.join(app.config['UPLOAD_FOLDER'],post.photo), "caption":post.caption,"created_on":strf_time(post.created_on, "%d %B %Y"),"likes":likes_amt}
        postList.append(p)
    return jsonify(postList=postList)

@app.route("/api/users/<int:user_id>/posts", methods=['GET','POST'])
@authenticate
def posts(user_id):
    if request.method == 'GET':
        user=UserProfile.query.filter_by(user_id=user_id).first()
        post=Post.query.filter_by(user_id=user_id).all()
        follower_amt=len(Follow.query.filter_by(user_id=user_id).all())
        respond={"status":"ok", "post_data":{"first_name":user.first_name, "lastname": user.last_name, "location": user.location, "joined_on": "Joined On"+strf_time(user.joined_on, "%B %Y"), "biography": user.biography, "postCount": len(posts), "followers": follower_amt, "profile_image": os.path.join(app.config['UPLOAD_FOLDER'],user.profile_photo), "posts":[]}}
    
    for i in post:
        postObj={"id":post_id, "user_id":post.user_id, "photo":os.path.join(app.config['UPLOAD_FOLDER'],post.photo), "caption":post.caption,"created_on":post.created_on}
        respond["post_data"]["post"].append(postObj)
    return jsonify(respond)
            
    if request.method =="POST":
        form=PostForm()
        if form.validate_on_submit():
            user_id=form.user_id.data
            photo=form.photo.data
            caption=form.caption.data
            
            user=UserProfile.query.filter_by(id=user_id).first()
            filename=user.username+secure_filename(photo.filename)
            created_on=str(datetime.date.today())
            post=Post(user_id=user_id,photo=photo,caption=caption,created_on=created_on)
            photo.save(os.path.join("./app",app.config['POST_IMG_UPLOAD_FOLDER'],filename))
            db.session.add(post)
            db.session.commit()
            return jsonify(status=201, message="Post created successfully")
        print form.errors.items()
        return jsonify(status=200, errors=form_errors(form))
    
        
@app.route("/api/users/<int:user_id>/follow", method=["POST"])
def follow(user_id):
    u =request.get_json()
    f=Follow.query.filter_by(user_id= u['user_id']).first()
    if f!= None:
        return jsonify(status = 200, message="Error")
    follow=Follow(user_id=u['user_id'], follower_id=u['follower_id'])
    db.session.add(follow)
    db.session.commit()
    
    return jsonify(status = 201, message="Success")
    

@app.route("/api/posts/<int:post_id>/like", method=["POST"])     
def like(post_id):
    request_payload=request.get_json()
    user_id=request_payload["user_id"]
    post_id=request_payload["post_id"]
    
    post=Post.query.filter_by(post_id=post_id)
    pLike=Like.query.filter_by(post_id=post_id).all()
    
    if post is None:
        return jsonify(status="", message="Post does not exist")
    
    if pLike is not None:
        for i in pLike:
            if i.user_id ==user_id:
                return jsonify(status=200, message="")
    
    like=Like(post_id=post_id, user_id=user_id)
    db.session.add(like)
    db.session.commit()
    like_amt=len(Like.query.filter_by(post_id=post_id).all())
    return jsonify({"status":201,"message":"liked post","likes":like_amt})

def strf_time(date, dateFormat):
    return datetime.date(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2])).strftime(dateFormat)

def form_errors(form):
    errorArr=[]
    for field,errors in form.errors.items():
        for error in errors:
            errorArr.append(error)
    return errorArr
    
    
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")        
        
        
        
        
        
        
        
        
        