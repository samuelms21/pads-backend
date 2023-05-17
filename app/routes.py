from flask import jsonify, request
from app import app, db
from app.models import SalesPerson, Customer, Products, Category, Orders, OrderDetails, Status
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/salespeople/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    try:
        sales_person = db.session.execute(db.select(SalesPerson).filter_by(username=username)).scalar_one()
        if check_password_hash(sales_person.password_hash, password):
            access_token = create_access_token(identity=sales_person.username)
            return jsonify({'access_token': access_token}), 200
    except:
        return jsonify({'message': 'Invalid credentials'}), 401 


# Example protected route
@app.route('/protected', methods=['GET'])
@jwt_required()  # Apply token validation
def protected_route():
    current_user = get_jwt_identity()  # Get the identity from the token
    return jsonify({'message': 'Protected route', 'user': current_user}), 200


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

# Get Salespeople Detail
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
    
    customer_id = data["customer_id"]
    cart = data["cart"]
    print(f"Customer ID: {customer_id}")
    print(f"Shopping cart: {cart}, type: {type(cart)}")

    # Create the order and order detail object (database)
    # status_id : 1 ( ACTIVE / IN-PROCESS )
    # status_id : 2 ( SENT )
    # status_id : 3 ( CANCELLED )
    new_order = Orders(_status_id=1, _customer_id=int(customer_id))
    db.session.add(new_order)
    db.session.commit()

    latest_id = db.session.execute(db.select(Orders).order_by(Orders.date.desc())).scalar_one().id
    
    for item in cart:
        new_order_detail = OrderDetails(item["product_id"], latest_id, item["product_qty"])
        db.session.add(new_order_detail)
    
    db.session.commit()

    return jsonify({"message": "Order created succesfully!"})


# Cancel Order
@app.route('/orders/cancel', methods=['PUT'])
def cancel_order():
    return "Cancel Order"