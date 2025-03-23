from flask import Flask, render_template, request
app = Flask(__name__)

# Global dictionary to hold user data (in-memory for simplicity)
budget_data = {
    "income": 0,
    "expenses": []
}

@app.route('/')
def index():
    # Pass the budget data to the frontend
    total_expenses = sum(expense['amount'] for expense in budget_data["expenses"])
    remaining_balance = budget_data["income"] - total_expenses
    return render_template('index.html',
                           income=budget_data["income"],
                           expenses=budget_data["expenses"],
                           total_expenses=total_expenses,
                           remaining_balance=remaining_balance)

@app.route('/add_income', methods=['POST'])
def add_income():
    income = request.form['income']
    if income:
        budget_data["income"] = float(income)
    return index()

@app.route('/add_expense', methods=['POST'])
def add_expense():
    expense_name = request.form['expense_name']
    expense_amount = request.form['expense_amount']
    if expense_name and expense_amount:
        budget_data["expenses"].append({
            "name": expense_name,
            "amount": float(expense_amount)
        })
    return index()

if __name__ == "__main__":
    app.run(debug=True)
