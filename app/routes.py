from flask import jsonify, request
from app import app, db, jwt
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

# Fetch all salespeople
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

# Get Salespeople Detail (CUSTOMER LIST BASED ON SALESPERSON)
@app.route('/salespeople/<int:id>', methods=['GET'])
@jwt_required()
def salesperson_detail(id):
    current_user = get_jwt_identity()
    sales = db.get_or_404(SalesPerson, id)
    customers = sales.customers.all()
    _customers = []
    for cust in customers:
        _cust = {
            "id": cust.id,
            "name": cust.name,
            "address": cust.address,
            "order_history": []
        }
        print("Customer ID:", cust.id)
        for order in list(cust.orders.all()):
            order_status = db.session.execute(db.select(Status).filter_by(id=order.status_id)).scalar_one().status
            order_instance = {
                "order_id": order.id,
                "order_status": order_status,
                "order_detail": []
            }
            order_details = list(order.order_details.all())
            total_order_purchase = 0
            for order_detail in order_details:
                product = db.session.execute(db.select(Products).filter_by(id=order_detail.product_id)).scalar_one()
                total_order_purchase += product.price * order_detail.product_qty
                order_instance["order_detail"].append(
                    {
                        "product_name": product.name,
                        "product_qty": order_detail.product_qty,
                        "product_price": product.price,
                        "product_sales": product.price * order_detail.product_qty
                    }
                )
            # print("Total Order Purchase:", total_order_purchase)
            order_instance["total_purchase"] = total_order_purchase
            order_instance["date"] = order.date
            _cust["order_history"].append(order_instance)

        _customers.append(_cust)

    s_detail = {
        "id": sales.id,
        "username": sales.username,
        "customers": _customers
    }
    return jsonify(s_detail)

# Error handling for invalid tokens
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Invalid token.", "error": str(error)}), 401

# Create Order (Protected)
@app.route('/orders/create', methods=['POST'])
@jwt_required()
def create_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    customer_id = data["customer_id"]
    cart = data["cart"]

    # Create the order and order detail object (database)
    # status_id : 1 ( ACTIVE / IN-PROCESS )
    # status_id : 2 ( SENT )
    # status_id : 3 ( CANCELLED )
    new_order = Orders(_status_id=1, _customer_id=int(customer_id))
    db.session.add(new_order)
    db.session.commit()

    recent_order_instance = db.session.execute(db.select(Orders).order_by(Orders.date.desc())).scalars()
    latest_order_id = list(recent_order_instance)[0].id
    print("Latest Order ID: ", latest_order_id)

    
    for item in cart:
        new_order_detail = OrderDetails(item["product_id"], latest_order_id, item["product_qty"])
        db.session.add(new_order_detail)
    
    db.session.commit()

    return jsonify({"message": "Order created succesfully!"}), 200


# Cancel Order
@app.route('/orders/cancel', methods=['PUT'])
@jwt_required()
def cancel_order():
    current_user = get_jwt_identity()
    return "Cancel Order"