from app import app, db
from app.models import SalesPerson, Customer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'SalesPerson': SalesPerson, 'Customer': Customer}