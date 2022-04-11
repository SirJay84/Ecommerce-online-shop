from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import Form,StringField,IntegerField,TextAreaField,validators

class AddProductForm(Form):
    name = StringField('Name:',[validators.DataRequired()])
    price = IntegerField('Price:',[validators.DataRequired()])
    discount = IntegerField('Discount:',default=0)
    stock = IntegerField('Stock:',[validators.DataRequired()])
    description = TextAreaField('Description:',[validators.DataRequired()])
    color = StringField('Color:',[validators.DataRequired()])

    image_1 = FileField('Image_1:',validators=[FileAllowed(['jpg','gif','png','jpeg'],'Images only')])
    image_2 = FileField('Image_2:',validators=[FileAllowed(['jpg','gif','png','jpeg'],'Images only')])
    image_3 = FileField('Image_3:',validators=[FileAllowed(['jpg','gif','png','jpeg'],'Images only')])

