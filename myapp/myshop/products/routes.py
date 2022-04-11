from flask import redirect,render_template,request,url_for,flash,session,current_app
from myapp.myshop import app,db,photos,search
from .models import Brand,Category,AddProduct
from .forms import AddProductForm
import secrets,os

def brands():
    brands = Brand.query.join(AddProduct, (Brand.id==AddProduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(AddProduct,(Category.id==AddProduct.category_id)).all()
    return categories

@app.route('/')
def home():
    products = AddProduct.query.filter(AddProduct.stock > 0)
    return render_template('products/index.html',products=products,brands=brands(),categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = AddProduct.query.msearch(searchword, fields=['name', 'description','color'], limit=3)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

"""Single_page route"""
@app.route('/product/<int:id>')
def single_page(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    product = AddProduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product,brands=brands(),categories=categories()) 

@app.route('/brand/<int:id>')
def get_brand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brand = AddProduct.query.filter_by(brand_id=id)
    return render_template('products/index.html',brand=brand,brands=brands(),categories=categories())

@app.route('/category/<int:id>/')
def get_category(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    category = AddProduct.query.filter_by(category_id=id)
    return render_template('products/index.html',category=category,categories=categories(),brands=brands())

@app.route('/addbrand', methods=['POST','GET'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        get_brand = request.form.get('brand')
        brand = Brand(name=get_brand)
        db.session.add(brand)
        db.session.commit()
        flash(f'{get_brand} brand has been added successfully to the database.','success')
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=['POST','GET'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    update_brand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        update_brand.name = brand
        db.session.commit()
        flash(f'Your brand has been updated.','success')
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand page', update_brand=update_brand)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} has been deleted.','success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cannot be deleted.','warning')
    return redirect(url_for('admin'))

@app.route('/addcat', methods=['POST','GET'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        get_brand = request.form.get('category')
        cat = Category(name=get_brand)
        db.session.add(cat)
        db.session.commit()
        flash(f'{get_brand} category has been added successfully to the database.','success')
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/updatecat/<int:id>', methods=['POST','GET'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    update_cat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        update_cat.name = category
        db.session.commit()
        flash(f'Your category has been updated successfully.','success')
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update Category page', update_cat=update_cat)

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} has been deleted.','success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} cannot be deleted.','warning')
    return redirect(url_for('admin'))

@app.route('/addproduct', methods=['POST','GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductForm(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        color = form.color.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        add_product = AddProduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            color=color,
            description=description,
            brand_id=brand,
            category_id=category,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3,
        )
        db.session.add(add_product)
        db.session.commit()
        flash(f'{name} has been added successfully to the database.','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html',title='Add Product page',form=form,brands=brands,categories=categories)

@app.route('/updateproduct/<int:id>', methods=['POST','GET'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    product = AddProduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = AddProductForm(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.color = form.color.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/images/'+ product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/images/'+ product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/images/'+ product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Your product has been updated.','success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.description
    return render_template('products/updateproduct.html', form=form,brands=brands,categories=categories,product=product)
    
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    product = AddProduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path,'static/images/'+ product.image_1))
            os.unlink(os.path.join(current_app.root_path,'static/images/'+ product.image_2))
            os.unlink(os.path.join(current_app.root_path,'static/images/'+ product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted.','success')
        return redirect(url_for('admin'))
    flash(f'The product {product.name} cannot be deleted.','warning')
    return redirect(url_for('admin'))