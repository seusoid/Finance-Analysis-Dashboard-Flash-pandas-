from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from extensions import db


app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

from models import Category, Expense  # import models AFTER db

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        category_name = request.form["category"]
        description = request.form["description"]
        payment_method = request.form["payment_method"]

        # Check if category already exists
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        expense = Expense(
            amount=amount,
            date=date,
            category_id=category.id,
            description=description,
            payment_method=payment_method
        )

        db.session.add(expense)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_expense.html")

@app.route("/view")
def view_expenses():
    # Query all expenses
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template("view_expenses.html", expenses=expenses)

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    if request.method == "POST":
        expense.amount = float(request.form["amount"])
        expense.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        category_name = request.form["category"]
        expense.description = request.form["description"]
        expense.payment_method = request.form["payment_method"]

        # Update or create category
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        expense.category_id = category.id

        db.session.commit()
        return redirect(url_for("view_expenses"))

    return render_template("edit_expense.html", expense=expense)


@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("view_expenses"))

from analysis import get_expenses_df, plot_category_totals, plot_monthly_trends

@app.route("/dashboard")
def dashboard():
    df = get_expenses_df()
    category_chart = plot_category_totals(df)
    monthly_chart = plot_monthly_trends(df)
    return render_template("dashboard.html",
                           category_chart=category_chart,
                           monthly_chart=monthly_chart)


if __name__ == "__main__":
    app.run(debug=True)
