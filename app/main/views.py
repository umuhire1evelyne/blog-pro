from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import getQuotes
from .forms import UpdateProfile,PostForm,CommentForm,UpdateForm
from ..models import User,PhotoProfile,Post,Comment
from flask_login import login_required,current_user
from .. import db,photos
import requests
import datetime
import markdown2


# Views
@main.route('/')
def index():
     quotes = getQuotes()


     return render_template('index.html',quotes=quotes)

@main.route('/all_posts/',methods = ['GET','POST'])
def all_posts():
     post = Post.query.all()

     return render_template('all_posts.html',post = post)

@main.route('/subscribe')
def subscribe():
    return render_template('subcribe.html',title='Subscribe')



@main.route('/profile/update/<int:post_id>',methods = ['GET','POST'])
@login_required
def update_post(post_id):
    users = Post.query.filter_by(id=post_id).first()
    if users is None:
        abort(404)
    user = current_user
    form = UpdateForm()

    if form.validate_on_submit():
        users.author = form.author.data
        users.description = form.description.data
        users.category = form.category.data
        db.session.add(users)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, user = user)



@main.route('/posts/new/', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        description = form.description.data
        author = form.author.data
        user_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_post = Post(user_id =current_user._get_current_object().id, author = author,description=description,category=category)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('main.all_posts'))
    return render_template('posts.html',form=form)



@main.route('/delete_post/<int:post_id>',methods= ['POST','GET'])
@login_required
def delete_post(post_id):
    post= Post.query.filter_by(id = post_id).first()
    post.delete_post()
    
    
    return redirect(url_for('main.all_posts'))

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('posts.html', author=post.author, post=post,comments=comments)

@main.route('/comment/new/<int:post_id>', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post=Post.query.get(post_id)
    if form.validate_on_submit():
        content = form.content.data
       
        new_comment = Comment(content = content, name = current_user._get_current_object().id, post_id = post_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', post_id= post_id))

    all_comments = Comment.query.filter_by(post_id = post_id).all()
    return render_template('comments.html', form = form, comment = all_comments, post = post )




@main.route('/delete_comment/<int:post_id>',methods= ['POST','GET'])
@login_required
def delete_comment(post_id):
    comment= Comment.query.filter_by(post_id = post_id).first()
    comment.delete_comment()
    
    
    return redirect(url_for('main.profile',post_id=post_id))          
    

@main.route('/user/<uname>')

def profile(uname):
    user = User.query.filter_by(username = uname).first()
    get_posts = Post.query.filter_by(user_id = current_user.id).all()
    print(get_posts)
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, posts = get_posts)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))