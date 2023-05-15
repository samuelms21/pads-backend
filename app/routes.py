from flask import jsonify
from app import app, db
from app.models import SalesPerson, Customer

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/salespeople')
def salespeople_list():
    salespeople = db.session.execute(db.select(SalesPerson).order_by(SalesPerson.id)).scalars()
    result = []
    for sales in salespeople:
        _sales = {
            "id": sales.id,
            "username": sales.username,
        }
        result.append(_sales)
    return jsonify(result)

@app.route('/sales/<int:id>')
def salesperson_detail(id):
    sales = db.get_or_404(SalesPerson, id)
    customers = sales.customers.all()
    _customers = []
    for cust in customers:
        _cust = {
            "id": cust.id,
            "name": cust.name,
            "address": cust.address,
        }
        _customers.append(_cust)
    s_detail = {
        "id": sales.id,
        "username": sales.username,
        "customers": _customers
    }
    return jsonify(s_detail)