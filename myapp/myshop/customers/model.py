from myapp.myshop import db,login_manager
from datetime import datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(user_id)

class Customer(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(180), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    zipcode = db.Column(db.String(50), nullable=False)
    profile = db.Column(db.String(255), nullable=False, default='profile.jpg')
    date_created = db.Column(db.DateTime(), nullable=False, default= datetime.utcnow)
    
    def __repr__ (self):
        return '<Customer: {}>'.format(self.username)

"""Inserting Dictionary into the database"""
class JSONEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self,value,dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self,value,dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(50), nullable=False, unique=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    customer_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.Column(JSONEncodedDict)

    def __repr__(self):
        return '<CustomerOrder: {}>'.format(self.invoice)

db.create_all()




