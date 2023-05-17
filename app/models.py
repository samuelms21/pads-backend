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

    def __init__(self, _name, _address, _salesperson_id):
        self.name = _name
        self.address = _address
        self.salesperson_id = _salesperson_id

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

    def __init__(self, _name, _price, _warehouse_qty, _active_qty, _available_qty, _category_id, _img_src):
        self.name = _name
        self.price = _price
        self.warehouse_qty = _warehouse_qty
        self.active_qty = _active_qty
        self.available_qty = _available_qty
        self.category_id = _category_id
        self.img_src = _img_src

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(256))
    products = db.relationship('Products', backref='category', lazy='dynamic')

    def __init__(self, _category_name):
        self.category_name = _category_name

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.Date, default=date.today)

    def __init__(self, _status_id, _customer_id):
        self.status_id = _status_id
        self.customer_id = _customer_id

    def __repr__(self):
        return f"Order ID: {self.id}, Status: {self.status_id},\nCustomerID: {self.customer_id}, Date: {self.date}"

class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_qty = db.Column(db.Integer)

    def __init__(self, _product_id, _order_id, _product_qty):
        self.product_id = _product_id
        self.order_id = _order_id
        self.product_qty = _product_qty

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), unique=True)

    def __init__(self, _status):
        self.status = _status