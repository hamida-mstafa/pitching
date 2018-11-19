from flask import render_template,request,flash,redirect,url_for
from . import main
from flask_login import login_required,current_user
from app.models import User,pitches,Comments
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
'test':TestConfig
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
    tech = pitches.query.filter_by(category='Technology').all()

    return render_template('index.html', title= title,posts=posts, tech=tech)




@main.route('/index', methods=['GET', 'POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = pitches(body=form.post.data, author=current_user, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    posts = pitches.retrieve_posts(id).all()

    return render_template("posts.html", title='Home Page', form=form,posts=posts)

@main.route('/post', methods = ['GET','POST'])
@login_required
def post():
   form = PostForm()
   if form.validate_on_submit():
       post = form.post.data
       category = form.category.data
       user = current_user


       new_pitches = pitches(body = post,category = category,user = user)

       # save pitches
       db.session.add(new_pitches)
       db.session.commit()

       return redirect(url_for('main.explore',uname = user.username))

   return render_template('post.html',form = form)


@main.route('/post/<int:id>', methods = ['GET','POST'])
@login_required
def user_post(id):

    users_post = pitches.query.filter_by(user_id=id).all()
    return render_template('user_posts.html',users_post = users_post)

@main.route('/technology' ,methods = ['GET','POST'])
def technology():
    technology = pitches.query.filter_by(category = 'Technology').all()
    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitches_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('technology.html', technology = technology,form=form)

@main.route('/sales' ,methods = ['GET','POST'])
def technolog():
    sales = pitches.query.filter_by(category = 'sales').all()
    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitches_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('sales.html', technology = technology,form=form)

@main.route('/interview' ,methods = ['GET','POST'])
def interview():
    interview = pitches.query.filter_by(category = 'Interview').all()

    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitches_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    return render_template('interview.html', interview = interview,form=form)
@main.route('/interview' ,methods = ['GET','POST'])
def business():
    business = pitches.query.filter_by(category = 'business').all()
    form = CommentForm()
    if form.validate_on_submit():
        details = form.details.data
        user = current_user

        new_comment = Comments(details = details,pitches_id=id,user =user)
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

        new_comment = Comments(details = details,pitches_id=id,user =user)
        # # save comment
        db.session.add(new_comment)
        db.session.commit()

    pickuplines = pitches.query.filter_by(category = 'Pickuplines').all()

    if pickuplines is None:
        abort(404)

    return render_template('pickuplines.html', pickuplines = pickuplines,form=form)



@main.route('/explore')
@login_required
def explore():
    posts = pitches.query.order_by(pitches.timestamp.desc()).all()
    return render_template('posts.html', title='Explore', posts=posts)


@main.route('/comments/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    comment = Comments.query.filter_by(pitches_id=id).all()

    form_comment = CommentForm()
    if form_comment.validate_on_submit():
        details = form_comment.details.data

        new_comment = Comments(details = details,pitches_id=id,user=current_user)
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
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('auth.user_profile',username=username))

# @login_required
# def post():
#     form = PostForm()
#     if form.validate_on_submit():
#         pitcheses = pitches(body=form.post.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash(_('Your post is now live!'))
#         return redirect(url_for('index'))
#     page = request.args.get('page', 1, type=int)
#     pitcheses = current_user.followed_pitcheses().paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('index', page=pitcheses.next_num) \
#         if pitcheses.has_next else None
#     prev_url = url_for('index', page=pitcheses.prev_num) \
#         if pitcheses.has_prev else None
#     return render_template('index.html', title=_('Home'), form=form,
#                            pitcheses=pitcheses.items, next_url=next_url,
#                            prev_url=prev_url)

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
