from flask import render_template,redirect,url_for,flash,request
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from .. import db
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')

    title = "Jobcornerlogin"
    return render_template('auth/login.html',login_form = login_form,title=title)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, bio = form.bio.data, password = form.password.data,role_id=2)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)
    
@auth.route('/create_admin/<uname>',methods=['GET','POST'])
def create_admin(uname):
    form=RegistrationForm()
    creator=User.query.filter_by(username=uname).first()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,bio = form.bio.data,password=form.password.data,role_id=1)

        user.save_user()
        flash('Admin Created','success')
        return redirect(url_for('main.profile',uname=creator.username))

    title='New blog Account'
    return render_template('auth/register_admin.html',form=form,title=title) 
