from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError
from wtforms.validators import Required,Email
from ..models import User

class PostForm(FlaskForm):
	author = StringField('Author', validators=[Required()])
	description = TextAreaField("Post a Blog Now :",validators=[Required()])
	category = StringField('Category', validators=[Required()])
	submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
	author = StringField('Author', validators=[Required()])
	description = TextAreaField("Edit your Blog Now :",validators=[Required()])
	category = StringField('Category', validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	name = StringField('Author', validators=[Required()])
	content = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself.',validators = [Required()])
    submit = SubmitField('Submit')