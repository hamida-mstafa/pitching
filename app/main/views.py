from flask import render_template,request,flash,redirect,url_for
from . import main
from flask_login import login_required,current_user
from app.models import User,Pitches,Comments
from datetime import datetime
from app import db, photos
from .forms import PostForm,CommentForm

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@main.route('/')
# @login_required
def index():

    title = 'Welcome to woo'
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
    ]
    pitches = Pitches.query.all()

    return render_template('index.html', title= title,posts=posts, pitches=pitches)




@main.route('/index', methods=['GET', 'POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Pitches(body=form.post.data, author=current_user, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    posts = Pitches.retrieve_posts(id).all()

    return render_template("posts.html", title='Home Page', form=form,posts=posts)

@main.route('/post', methods = ['GET','POST'])
@login_required
def post():
   form = PostForm()
   if form.validate_on_submit():
       post = form.post.data
       category = form.category.data
       user = current_user

       new_pitch = Pitches(body = post,category = category)

       # save pitch
       db.session.add(new_pitch)
       db.session.commit()

       return redirect(url_for('main.explore',uname = user.username))

   return render_template('post.html',form = form)


@main.route('/post/<int:id>', methods = ['GET','POST'])
@login_required
def user_post(id):

    users_post = Pitches.query.filter_by(user_id=id).all()
    return render_template('user_posts.html',users_post = users_post)

@main.route('/technology' ,methods = ['GET','POST'])
def technology():
    technology = Pitches.query.filter_by(category = 'Technology').all()
    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitch_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('technology.html', technology = technology,form=form)

@main.route('/sales' ,methods = ['GET','POST'])
def technolog():
    sales = Pitches.query.filter_by(category = 'Sales').all()
    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitch_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('sales.html', sales = sales,form=form)

@main.route('/interview' ,methods = ['GET','POST'])
def interview():
    interview = Pitches.query.filter_by(category = 'Interview').all()

    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitch_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('interview.html', interview = interview,form=form)
@main.route('/business' ,methods = ['GET','POST'])
def business():
    business = Pitches.query.filter_by(category = 'Business').all()
    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitch_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('business.html', business = business,form=form)

@main.route('/pickuplines' ,methods = ['GET','POST'])
def pickuplines():

    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitch_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    pickuplines =Pitches.query.filter_by(category = 'Pickup').all()

    if pickuplines is None:
        abort(404)

    return render_template('pickuplines.html', pickuplines = pickuplines,form=form)



@main.route('/explore')
@login_required
def explore():
    posts = Pitches.query.order_by(Pitches.timestamp.desc()).all()
    return render_template('posts.html', title='Explore', posts=posts)


@main.route('/comments/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    comment = Comments.query.filter_by(pitch_id=id).all()

    form_comment = CommentForm()
    if form_comment.validate_on_submit():
        details = form_comment.details.data

        new_comment = Comments(details = details,Pitches_id=id,user=current_user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('comments.html',form_comment = form_comment,comment=comment)
@main.route('/user/<username>/update/pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
    return redirect(url_for('auth.user_profile',username=username))


@main.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author':user, 'body':'test Post#1'
        }
    ]
    return render_template('profile/user_profile.html',posts=posts, user=user)
    '''
    i have used a variant of first() called fist_or_404()
    which works exactly like first() when there are results, and in case there
    are no results it auto sends a 404 error back
    '''
