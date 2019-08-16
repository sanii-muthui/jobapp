from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required

class PostAPitch (FlaskForm):
	title = StringField('Add Title', validators=[Required()])
	description = TextAreaField("Add Description:",validators=[Required()])
	category = RadioField('Cataegory', choices=[ ('Technology','Technology'), ('Education','Education'),('Music','Music'),('Animation','Animation')],validators=[Required()])
	company = StringField("Add Company:",validators=[Required()])
	state = StringField("Add state:",validators=[Required()])
	qualifications = TextAreaField("Add qualifications:",validators=[Required()])
	submit = SubmitField('Submit Blog')

class CommentForm(FlaskForm):
	description = TextAreaField('Leave a Comment?',validators=[Required()])
	submit = SubmitField()

class UpdateBio(FlaskForm):
    bio = StringField("Bio")
    submit = SubmitField("Update")
