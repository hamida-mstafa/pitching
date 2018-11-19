from flask import render_template,request,flash,redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from . import auth
from .forms import LoginForm,EditProfileForm, RegistrationForm,ResetPasswordRequestForm
from app import db
from datetime import datetime
from app.email import *
from ..email import mail_message

#Registration route section#
@auth.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successfull!')
        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


    '''
    first I ensure that the user that invokes this route is
    not logged in. Logic inside if validate_on_submit() creates a
    new user with the username, email and password provide, writes it to the db
    and then redirects to the login prompt so that the user can ogin


    '''
#End Registration route section#





############Log in section##############
'''
The user log in is facilitated by Flask-Login's login_user() function, the value
of the next query string argument is obtained. Flask provides a request variable that
contains all the info that the client sent with the request.
request.args attribute exposes the contents of the query string in a friendly dictionary format
'''

@auth.route('/login', methods=['GET','POST'])
# @login_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!= '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sig In', form = form)
    '''
    First step is to load the user from the db,then query
    the db with the log in username to find the user.
    the result of filetr_by is a query that only
    includes the objects that have a matching username
    since there is only going to be one or zero user results,
    I use first() which will return the user object if it exists,
    or None if it does not.
    first() method is another commonly used way to
    execute a query, when you only need to have
    one result
    Also I call the check_password() method to determine if the password entered in the form matches the hash or not

    '''
############End Log in section##############


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

    '''
    offers users the option to log out of the application
    '''
###############Log out route end##############

###############User_profile route end##############

@auth.route('/user/<username>')
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

@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.username.data  = current_user.username
        form.about_me.data = current_user.bio

    return render_template('profile/edit_profile.html', title='Edit Profile', form=form)
    '''
    If validate_on_submit() returns True the data is copied from the form into the user object and then writen the object to the database.
    '''

    ###############End user profile route##############


# @auth.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_password_reset_email(user)
#         flash('Check your email for the instructions to reset your password')
#         return redirect(url_for('auth.login'))

#     return render_template('email/reset_password_request.html',title='Reset Password', form=form)
#     '''
#     first, i make sure the user is not logged in,when the form is submitted and valid, i look up the user email provided in the form
#     ,if the user is found, a password reset email will be sent using
#     send_password_reset_email()
#     '''

    #########Rsetting password######

# @auth.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset.')
#         return redirect(url_for('auth.login'))
#     return render_template('email/reset_paword.html', form=form)
