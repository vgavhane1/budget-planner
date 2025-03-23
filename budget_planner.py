import cgi

# Function to calculate remaining balance
def calculate_balance(income, expenses):
    total_expenses = sum(expenses)
    remaining_balance = income - total_expenses
    return total_expenses, remaining_balance

def main():
    # Set up the form to receive input from HTML
    form = cgi.FieldStorage()

    # Get income and expense data from form
    try:
        income = float(form.getvalue('income'))
    except (TypeError, ValueError):
        income = 0

    expense_name = form.getvalue('expense_name')
    try:
        expense_amount = float(form.getvalue('expense_amount'))
    except (TypeError, ValueError):
        expense_amount = 0

    # Store expenses (you can expand this to store multiple expenses)
    expenses = [expense_amount]

    # Calculate total expenses and remaining balance
    total_expenses, remaining_balance = calculate_balance(income, expenses)

    # Output HTML response
    print("Content-type: text/html\n")
    print(f"<html><body>")
    print(f"<h1>Budget Planner Summary</h1>")
    print(f"<p>Income: ${income}</p>")
    print(f"<p>Total Expenses: ${total_expenses}</p>")
    print(f"<p>Remaining Balance: ${remaining_balance}</p>")
    print(f"<h3>Expense List:</h3>")
    print(f"<ul>")
    for expense in expenses:
        print(f"<li>{expense_name}: ${expense}</li>")
    print(f"</ul>")
    print(f"</body></html>")

if __name__ == "__main__":
    main()
