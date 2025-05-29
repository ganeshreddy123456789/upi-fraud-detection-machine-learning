from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import csv

app = Flask(__name__)

# Load Dataset
df = pd.read_csv("dataset.csv")

# Features & Labels
feature_columns = ["Amount"]
label_column = "Fraud"

# Train Random Forest Model
def train_fraud_model(data):
    X = data[feature_columns]
    y = data[label_column]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model

model = train_fraud_model(df)

# Transaction Categories
categories = [
    "Merchant Payment", "Friend Transfer", "Bill Payment",
    "Subscription", "Loan Repayment", "Online Shopping",
    "Salary Transfer", "Gift Payment"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        transaction_id = request.form["transaction_id"]
        sender = request.form["sender"]
        receiver = request.form["receiver"]
        upi_id = request.form["upi_id"]
        amount = float(request.form["amount"])
        status = request.form["status"]
        category = request.form["category"]

        # Predict Fraud using Random Forest
        prediction = model.predict([[amount]])
        is_fraud = "❌ Fraudulent Transaction" if prediction[0] == 1 else "✅ Legit Transaction"

        # Save transaction to CSV
        with open("dataset.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([transaction_id, sender, receiver, upi_id, amount, status, category, prediction[0]])

        # Retrain Model with New Data
        df_new = pd.read_csv("dataset.csv")
        
        # Update model without using `global`
        updated_model = train_fraud_model(df_new)

        return render_template("index.html", result=is_fraud, categories=categories)

    return render_template("index.html", result=None, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
