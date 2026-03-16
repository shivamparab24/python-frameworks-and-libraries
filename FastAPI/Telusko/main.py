# def greet():
#     print("Welcome User!")

# greet()


from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from FastAPI.Telusko import database_model
from FastAPI.Telusko.models import Product
from FastAPI.Telusko.config import session, engine


app = FastAPI()
database_model.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origin = ["http://localhost:3000"],
    allow_methods = ["*"]
)

@app.get("/")
def greet():
    return "Welcome User!!"


# products = [
#     Product(1, "Phone", "A smartphone", 699.99, 50),
#     Product(2, "Laptop", "A powerful laptop", 999.99, 30),
#     Product(3, "Pen", "A blue ink pen", 1.99, 100),
#     Product(4, "Table", "A wooden table", 199.99, 20),
#     Product(5, "Headphones", "Noise cancelling headphones", 149.99, 40),
#     Product(6, "Keyboard", "Mechanical keyboard", 89.99, 35),
#     Product(7, "Mouse", "Wireless optical mouse", 29.99, 60),
#     Product(8, "Monitor", "24-inch LED monitor", 179.99, 25),
#     Product(9, "Notebook", "200-page ruled notebook", 4.99, 120),
#     Product(10, "Backpack", "Laptop travel backpack", 59.99, 45),
#     Product(11, "Charger", "65W fast charger", 24.99, 70),
#     Product(12, "USB Cable", "USB-C charging cable", 9.99, 150),
# ]

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
    Product(id=5, name="Headphones", description="Noise cancelling headphones", price=149.99, quantity=40),
    Product(id=6, name="Keyboard", description="Mechanical keyboard", price=89.99, quantity=35),
    Product(id=7, name="Mouse", description="Wireless optical mouse", price=29.99, quantity=60),
    Product(id=8, name="Monitor", description="24-inch LED monitor", price=179.99, quantity=25),
    Product(id=9, name="Notebook", description="200-page ruled notebook", price=4.99, quantity=120),
    Product(id=10, name="Backpack", description="Laptop travel backpack", price=59.99, quantity=45),
    Product(id=11, name="Charger", description="65W fast charger", price=24.99, quantity=70),
    Product(id=12, name="USB Cable", description="USB-C charging cable", price=9.99, quantity=150),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = session()
    count = db.query(database_model.Product).count
    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    #db_connection
    # db = session()
    # db.query()

    db_products = db.query(database_model.Product).all()

    return db_products
    # return products

# @app.get("/product/{id}")
# def get_product_by_id(id: int):
#     return products[id-1]


@app.get("/product/{id}")
# def get_product_by_id(id: int):
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"



@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    # products.append(product)
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id == id:
    #         products[i] = product
    #         return "Product Added"
    # return "No Product Found"
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        
        db.commit()  
        return "Product Updated"
    else:
        return "No product found"


@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id == id:
    #         del products[i]
    #         return "Product Deleted"
    # return "Product Not Found"

    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "Product Not Found"