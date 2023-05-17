from flask import jsonify, request
from app import app, db, login_manager
from app.models import SalesPerson, Customer, Products, Category, Orders, OrderDetails, Status
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@login_manager.user_loader
def load_user(id):
    return SalesPerson(id)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    return jsonify({"username": username, "password": password})


@app.route('/salespeople', methods=['GET'])
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

@app.route('/salespeople/<int:id>', methods=['GET'])
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

# Create Order
@app.route('/orders/create', methods=['POST'])
def create_order():
    data = request.get_json()
    # for key, value in data.items():
    #     print(key, value)
    
    customer_id = data["customer_id"]
    cart = data["cart"]
    print(f"Customer ID: {customer_id}")
    print(f"Shopping cart: {cart}")

    # Create the order and order detail object (database)
    # status_id : 1 ( ACTIVE / IN-PROCESS )
    new_order = Orders(1, int(customer_id))
    print("#"*50)
    print(new_order)    

    db.session.add(new_order)
    db.session.commit()

    # Create new order detail
    new_order_detail = OrderDetails()

    return jsonify(data)