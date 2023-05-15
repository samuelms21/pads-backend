from app import app, db
from app.models import SalesPerson, Customer, Products, Category, Orders, OrderDetails, Status

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'SalesPerson': SalesPerson, 'Customer': Customer, 'Products': Products, 'Category': Category, 'Orders': Orders, 'OrderDetails': OrderDetails, 'Status': Status}
