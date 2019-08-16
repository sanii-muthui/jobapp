from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required

class PostAPitch (FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("ADD BLOG:",validators=[Required()])
	category = RadioField('Label', choices=[ ('Technology','Technology'), ('Education','Education'),('Music','Music'),('Animation','Animation')],validators=[Required()])
	submit = SubmitField('Submit:)')

class CommentForm(FlaskForm):
	description = TextAreaField('What do you think?',validators=[Required()])
	submit = SubmitField()

class UpdateBio(FlaskForm):
    bio = StringField("Bio")
    submit = SubmitField("Update")
