from app import db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

class SalesPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    customers = db.relationship('Customer', backref='salesperson', lazy='dynamic')

    def __init__(self, _username, _password):
        self.username = _username
        self.password_hash = generate_password_hash(_password)

    def __repr__(self):
        return '<SalesPerson {}>'.format(self.username)
    
    def get_id(self):
        return str(self.id)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    address = db.Column(db.String(512))
    salesperson_id = db.Column(db.Integer, db.ForeignKey('sales_person.id'))
    orders = db.relationship('Orders', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f'<Customer {self.id}: {self.name}>'

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    price = db.Column(db.Float)
    warehouse_qty = db.Column(db.Integer)
    active_qty = db.Column(db.Integer)
    available_qty = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    img_src = db.Column(db.String(512))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(256))
    products = db.relationship('Products', backref='category', lazy='dynamic')

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.Date, default=date.today)

class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_qty = db.Column(db.Integer)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), unique=True)