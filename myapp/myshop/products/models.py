from myapp.myshop import db
from datetime import datetime

class AddProduct(db.Model):
    __searchable__ = ['name', 'description',]
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False,unique=True)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer,default=0)
    stock = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    image_1 = db.Column(db.String(150),nullable=False,default='image.jpg')
    image_2 = db.Column(db.String(150),nullable=False,default='image.jpg')
    image_3 = db.Column(db.String(150),nullable=False,default='image.jpg')

    brand = db.relationship('Brand', backref='add_product', lazy=True)
    category = db.relationship('Category', backref='add_product', lazy=True)

    def __repr__(self):
        return '<AddProduct: {}>'.format(self.name)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)

    
    def __repr__(self):
        return "<Brand: {}>".format(self.name)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)

    
    def __repr__(self):
        return "<Category: {}>".format(self.name)

db.create_all()

