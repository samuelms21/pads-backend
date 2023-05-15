from app import db

class SalesPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    customers = db.relationship('Customer', backref='salesperson', lazy='dynamic')

    def __repr__(self):
        return '<SalesPerson {}>'.format(self.username)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    address = db.Column(db.String(512))
    salesperson_id = db.Column(db.Integer, db.ForeignKey('sales_person.id'))

    def __repr__(self):
        return f'<Customer {self.id}: {self.name}>'