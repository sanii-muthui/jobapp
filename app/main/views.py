from flask import render_template,request,redirect,url_for,abort
from app import create_app
from . import main
from ..models import Pitch, User,Comment
from .forms import UpdateBio,PostAPitch, CommentForm
from flask_login import login_required, current_user
from .. import db,photos
from datetime import datetime
from flask.views import View,MethodView
#single user
import markdown2

# homepage function

@main.route('/', methods = ['GET','POST'])
def index():

    '''
    Root page functions that return the home page and its data
    '''
    pitch = Pitch.query.filter_by().first()
    title = 'JobCorner'
    Technology = Pitch.query.filter_by(category="Technology")
    Education = Pitch.query.filter_by(category = "Education")
    Music = Pitch.query.filter_by(category = "Music")
    Animation = Pitch.query.filter_by(category = "Animation")

    

    return render_template('home.html', title = title, pitch = pitch, Technology = Technology, Education = Education, Music = Music,Animation = Animation)
    
@main.route('/admin/pitches/new/', methods=['GET', 'POST'])
@login_required
def new_pitch():
    pitch_form = PostAPitch()
    if pitch_form.validate_on_submit():
         description = pitch_form.description.data
         title = pitch_form.title.data
         owner_id = current_user
         category = pitch_form.category.data
         print(current_user._get_current_object().id)
        # Updated pitch instance
         new_pitch = Pitch(owner_id =current_user.id, title = title,description=description,category=category)
         db.session.add(new_pitch)
         db.session.commit()
         title = 'New Pitch'
         return redirect(url_for('main.index'))
    return render_template('admin/pitches.html', pitch_form=pitch_form)



#@main.route('/pitches/<int:pitch_id>/delete',methods=['GET','POST'])
#@login_required
#def delete_entry(pitch_id):
    '''
    View function to delete a drift post
    '''
 #   pitch=Pitch.query.get_or_404(pitch_id)
  #  if pitch.author != current_user:
   #     abort(403)
        
    #db.session.delete(new_pitch)
    #db.session.commit()
    #flash('Post Deleted Successfully','success')
    
    #return redirect(url_for('/'))



@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', pitch_id= pitch_id))

    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comments.html', form = form, comment = all_comments, pitch = pitch )

    """ The above allows you to add a comment in all the categories of the different pitches"""


# user profile page function
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

#update profile
@login_required
@main.route('/user/<uname>/update',methods = ['GET','POST'])
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

# user login
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


