from app import app, db
from app.models import SalesPerson, Customer, Products, Category, Orders, OrderDetails, Status

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'SalesPerson': SalesPerson, 'Customer': Customer, 'Products': Products, 'Category': Category, 'Orders': Orders, 'OrderDetails': OrderDetails, 'Status': Status}

def reset_tables():
    with app.app_context():
        db.drop_all()
        db.session.commit()
        db.create_all()
        db.session.commit()

def create_tables():
    with app.app_context():
        # Salesperson
        sales_1 = SalesPerson("john_doe", "password")
        sales_2 = SalesPerson("peter_parker", "password")
        db.session.add(sales_1)
        db.session.add(sales_2)
        db.session.commit()
        
        # Customer
        cust_1 = Customer("cust_1", "Jakarta", 1)
        cust_2 = Customer("cust_2", "Bekasi", 1)
        cust_3 = Customer("cust_3", "Depok", 1)
        cust_4 = Customer("cust_4", "Tangerang", 2)
        cust_5 = Customer("cust_5", "Bogor", 2)
        cust_6 = Customer("cust_6", "Cibitung", 2)

        db.session.add(cust_1)
        db.session.add(cust_2)
        db.session.add(cust_3)
        db.session.add(cust_4)
        db.session.add(cust_5)
        db.session.add(cust_6)
        db.session.commit()

        # Category
        tech = Category("tech")
        fashion = Category("fashion")
        gaming = Category("gaming")
        db.session.add(tech)
        db.session.add(fashion)
        db.session.add(gaming)
        
        # Products
        # Tech
        iphone = Products("iPhone", 100, 100, 0, 100, 1, "iphone.png")
        samsung_phone = Products("Samsung", 90, 100, 0, 100, 1, "samsung.png")
        # Fashion
        tshirt = Products("T-shirt", 50, 100, 0, 100, 2, "tshirt.png")
        jeans = Products("Jeans", 40, 100, 0, 100, 2, "jeans.png")
        # Gaming
        razer = Products("Razer Laptop", 120, 100, 0, 100, 3, "razer_laptop.png")
        asus_rog = Products("ASUS ROG", 110, 100, 0, 100, 3, "asus_rog.png")
        db.session.add(iphone)
        db.session.add(samsung_phone)
        db.session.add(tshirt)
        db.session.add(jeans)
        db.session.add(razer)
        db.session.add(asus_rog)
        db.session.commit()

        # Order Status
        active = Status("active")
        sent = Status("sent")
        cancelled = Status("cancelled")
        db.session.add(active)
        db.session.add(sent)
        db.session.add(cancelled)
        db.session.commit()

if __name__ == "__main__":
    reset_tables()
    create_tables()
    app.run(debug=True)
