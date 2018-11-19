from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject,template,to,**kwargs):
    sender_email ='hamidamstafa@gmail.com'

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)

# from flask_mail import Message
# from app import mail
# from flask import render_template

# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)

# def send_password_reset_email(user):
#     token = user.get_reset_password_token()
#     send_email('[Microblog] Reset Your Password',
#                sender_email ='kibetedgar@gmail.com',
#                recipients=[user.email],
#                text_body=render_template('email/reset_password.txt',
#                                          user=user, token=token),
#                html_body=render_template('email/reset_password.html',
#                                          user=user, token=token))

#     '''
#     The template recive the user and the token as arguments,
#     so that a personalized email message can be genrated.
#     '''
