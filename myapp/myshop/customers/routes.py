from flask import redirect,render_template,request,url_for,flash,session,current_app,make_response
from myapp.myshop import app,db,photos,search,bcrypt,login_manager
from .forms import CustomerRegistrationForm,CustomerLoginForm
from myapp.myshop.customers.model import Customer,CustomerOrder
from flask_login import login_required,current_user,login_user, logout_user
import secrets
import os
import json
import pdfkit

@app.route('/customer/register', methods=['POST', 'GET'])
def customer_register():
    form = CustomerRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        customer = Customer(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            county=form.county.data,
            state=form.state.data,
            address=form.address.data,
            phone_number=form.phone_number.data,
            zipcode=form.zipcode.data
        )
        db.session.add(customer)
        db.session.commit()
        flash(f'Welcome {form.name.data},thank you for registering!','success')
        return redirect(url_for('customer_login'))

    return render_template('customer/register.html',form=form,title='Customer Registration page')

@app.route('/customer/login', methods=['POST','GET'])
def customer_login():
    form = CustomerLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password,form.password.data):
            login_user(customer)
            return redirect(url_for('home'))
        else:
            flash(f'Invalid email or password.','danger')
            return redirect(url_for('customer_login'))
    else:
        return render_template('customer/login.html',form=form,title='Customer Login page')

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect (url_for('home'))
    
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash(f'Your order has been created successfully.','success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash(f'Something went wrong with your order.','danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        subtotal = 0
        grandtotal = 0
        customer_id = current_user.id
        customer = Customer.query.filter_by(id=customer_id).first()
        order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for key, product in order.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ('%0.2f' % (.16 * float(subtotal)))
            grandtotal = float('%0.2f' % (1.16 * subtotal))
    else:
        return redirect(url_for('customer_login'))
    return render_template('customer/order.html', invoice=invoice,tax=tax,subtotal=subtotal,grandtotal=grandtotal,customer=customer,order=order)

@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        subtotal = 0
        grandtotal = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Customer.query.filter_by(id=customer_id).first()
            order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for key, product in order.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount
                tax = ('%0.2f' % (.16 * float(subtotal)))
                grandtotal = float('%0.2f' % (1.16 * subtotal))
            rendered = render_template('customer/pdf.html', invoice=invoice,tax=tax,grandtotal=grandtotal,customer=customer,order=order)
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdf = pdfkit.from_string(rendered,False, configuration=config)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename='+invoice+'.pdf'
            return response
        return request (url_for('orders'))


    