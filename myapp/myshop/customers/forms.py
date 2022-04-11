from wtforms import Form,StringField,PasswordField,SubmitField,validators,ValidationError
from flask_wtf.file import FileAllowed,FileField
from myapp.myshop.customers.model import Customer

class CustomerRegistrationForm(Form):
    name = StringField('Name:', [validators.Length(min=4, max=25)])
    username = StringField('Username:', [validators.Length(min=4, max=25)])
    email = StringField('Email Address:',[validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password:',[validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match!')])
    confirm = PasswordField('Repeat Password:',[validators.DataRequired()])

    county = StringField('County:', [validators.DataRequired()])
    state = StringField('State:',[validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])
    phone_number = StringField('Cell_number:', [validators.DataRequired()])
    zipcode = StringField('Zip code:', [validators.DataRequired()])

    profile = FileField('Profile:', validators=[FileAllowed(['jpg','jpeg','png','gif'],'Images only please!')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        if Customer.query.filter_by(username=username.data).first():
            raise ValidationError('Username already in use!')

    def validate_email(self,email):
        if Customer.query.filter_by(email=email.data).first():
            raise ValidationError('Email already in use!')

class CustomerLoginForm(Form):
    email = StringField('Email Address:',[validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password:',[validators.DataRequired()])
    





