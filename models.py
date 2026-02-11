from extensions import db
from datetime import date

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationship: One category → many expenses
    expenses = db.relationship('Expense', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(200))
    payment_method = db.Column(db.String(50))

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __repr__(self):
        return f"<Expense {self.amount}>"

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    category = db.relationship("Category", backref="budgets")

    def __repr__(self):
        return f"<Budget {self.amount} for {self.category.name} in {self.month}>"
