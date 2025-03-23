from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

USER_DATA_FILE = 'user_data.json'
BUDGET_DATA_FILE = 'budget_data.json'


def load_data(file):
    """ Load data from a JSON file. """
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}


def save_data(file, data):
    """ Save data to a JSON file. """
    with open(file, 'w') as f:
        json.dump(data, f)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        users = load_data(USER_DATA_FILE)

        if users.get(username) == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Invalid credentials!")
    
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    budget_data = load_data(BUDGET_DATA_FILE)
    
    if request.method == "POST":
        category = request.form.get("category")
        amount = float(request.form.get("amount"))
        
        if username not in budget_data:
            budget_data[username] = {"budget_items": []}
        
        budget_data[username]["budget_items"].append({"category": category, "amount": amount})
        save_data(BUDGET_DATA_FILE, budget_data)
    
    budget_items = budget_data.get(username, {}).get("budget_items", [])
    return render_template("dashboard.html", username=username, budget_items=budget_items)


@app.route("/report")
def report():
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    budget_data = load_data(BUDGET_DATA_FILE)
    
    budget_items = budget_data.get(username, {}).get("budget_items", [])
    return render_template("report.html", budget_items=budget_items)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
