from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DecimalField, FileField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import re
import os

project_choices_eng = [
    ('Residential Complex', 'Residential Complex'),
    ('Shopping Mall', 'Shopping Mall'),
    ('Office Tower', 'Office Tower'),
    ('Bridge Construction', 'Bridge Construction'),
    ('School Renovation', 'School Renovation'),
    ('Hospital Expansion', 'Hospital Expansion'),
    ('Highway Interchange', 'Highway Interchange'),
    ('Data Center Construction', 'Data Center Construction'),
    ('Water Treatment Plant', 'Water Treatment Plant'),
    ('Sports Stadium', 'Sports Stadium'),
    ('Urban Park Development', 'Urban Park Development'),
    ('Metro Rail System', 'Metro Rail System')
]
project_choices = [
    ('Stambeno naselje', 'Stambeno naselje'),
    ('Šoping centar', 'Šoping centar'),
    ('Poslovna zgrada', 'Poslovna zgrada'),
    ('Cestovni most', 'Cestovni most'),
    ('Renovacija škole', 'Renovacija škole'),
    ('Proširenje bolničkog krila', 'Proširenje bolničkog krila'),
    ('Autocesta ili državna cesta', 'Autocesta ili državna cesta'),
    ('Proizvodni pogon', 'Proizvodni pogon'),
    ('Pročistač otpadnih voda', 'Pročistač otpadnih voda'),
    ('Sporski stadion', 'Sporski stadion'),
    ('Novi urbani park', 'Novi urbani park'),
    ('Urbana željeznica', 'Urbana željeznica')
]
report_choices = [
    ('Environmental impact assessment', 'Environmental impact assessment'),
    ('Environmental and Social impact assessment', 'Environmental and Social impact assessment'),
    ('Scoping elaborate', 'Scoping elaborate'),
    ('Biodiversity impact report', 'Biodiversity impact report'),
    ('Climate risk report', 'Climate risk report')
]

geolocation_choices = [
    ('Pick a point', 'Pick a point'),
    ('Draw a polygon', 'Draw a polygon'),
    ('Upload geo file', 'Upload geo file')
]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    text_message = TextAreaField('text_message', validators=[Length(min=0, max=240)])
    submit = SubmitField('Submit')

class NewProjectForm(FlaskForm):
    project_title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Project summary', validators=[Length(min=0, max=220)])
    description = TextAreaField('Project description', validators=[Length(min=0, max=440)])
    project_type = SelectField('Select project type', choices=project_choices)
    report_type = SelectField('Select report type', choices=report_choices)
    experts = TextAreaField("Name your colaborators on this project", validators=[Length(min=0, max=220)])
    lat = DecimalField('Insert your lat coordinate of project')
    lon = DecimalField('Insert your lon coordinate of project')
    geo_file = FileField('Insert your geo data file')
    submit = SubmitField('Save project')

class EditProjectForm(FlaskForm):
    project_title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Project summary', validators=[Length(min=0, max=220)])
    description = TextAreaField('Project description', validators=[Length(min=0, max=440)])
    project_type = SelectField('Select project type', choices=project_choices)
    report_type = SelectField('Select report type', choices=report_choices)
    experts = TextAreaField("Name your colaborators on this project", validators=[Length(min=0, max=220)])

    lat = DecimalField('Insert your lat coordinate of project')
    lon = DecimalField('Insert your lon coordinate of project')
    # TODO: add fileField validators, or add MultipleFileField for shp file
    geo_file = MultipleFileField('Insert your geo data file')
    submit = SubmitField('Save project')

    class Meta:
        # Set the enctype attribute for the form
        enctype = 'multipart/form-data'

class UploadForm(FlaskForm):
    geo_file = FileField('Insert your geo data file')
    submit = SubmitField('Save the geo data file')
    class Meta:
        # Set the enctype attribute for the form
        enctype = 'multipart/form-data'

class DeleteProjectForm(FlaskForm):
    submit = SubmitField('Delete project')


class GeolocationForm(FlaskForm):
    geolocation_option = SelectField('Select where you want to locate your project', choices=geolocation_choices)
    submit = SubmitField('Get the location')

