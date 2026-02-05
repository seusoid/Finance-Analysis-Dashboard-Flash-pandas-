import pandas as pd
from models import Expense, Category
from extensions import db
import matplotlib.pyplot as plt
import seaborn as sns
import os

def get_expenses_df():
    """Fetch all expenses from DB and return as pandas DataFrame"""
    expenses = Expense.query.all()
    data = []
    for e in expenses:
        data.append({
            "id": e.id,
            "amount": e.amount,
            "date": e.date,
            "category": e.category.name,
            "description": e.description,
            "payment_method": e.payment_method
        })
    df = pd.DataFrame(data)

    # Convert 'date' to datetime
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df

def total_spending_by_category(df):
    return df.groupby("category")["amount"].sum()

def monthly_spending(df):
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")["amount"].sum()

def spending_by_day_of_week(df):
    df["day_of_week"] = df["date"].dt.day_name()
    return df.groupby("day_of_week")["amount"].sum()



def plot_category_totals(df):
    totals = df.groupby("category")["amount"].sum()
    plt.figure(figsize=(6,6))
    totals.plot.pie(autopct="%1.1f%%")
    plt.title("Spending by Category")
    chart_path = os.path.join("static", "charts", "category_totals.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def plot_monthly_trends(df):
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month")["amount"].sum()
    plt.figure(figsize=(8,4))
    monthly.plot(linewidth=2, marker="o")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    chart_path = os.path.join("static", "charts", "monthly_trends.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path