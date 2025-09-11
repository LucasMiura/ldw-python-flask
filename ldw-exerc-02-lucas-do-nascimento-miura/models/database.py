from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cloth(db.Model):
    __tablename__ = "clothes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, title, price, category, image, quantity=0):
        self.title = title
        self.price = price
        self.category = category
        self.image = image
        self.quantity = quantity