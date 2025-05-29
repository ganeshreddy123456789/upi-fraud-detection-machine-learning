import pandas as pd
import numpy as np
from faker import Faker
import random

faker = Faker('en_IN')  # Indian locale for realistic names

# Expanded Indian UPI ID domains
upi_domains = [
    "@ybl", "@paytm", "@upi", "@okhdfcbank", "@oksbi",
    "@okicici", "@okaxis", "@okkotak", "@okbob", "@okpnb"
]

# Transaction Categories
categories = [
    "Merchant Payment", "Friend Transfer", "Bill Payment",
    "Subscription", "Loan Repayment", "Online Shopping",
    "Salary Transfer", "Gift Payment"
]

# Generate Fake Data
def generate_fake_data(n=500):
    data = []
    for i in range(1, n+1):
        transaction_id = random.randint(1000000000, 9999999999)  # 10-digit numeric Transaction ID
        sender = faker.first_name() + " " + faker.last_name()  # Indian names
        receiver = faker.first_name() + " " + faker.last_name()
        upi_id = sender.split()[0].lower() + str(random.randint(1000, 9999)) + random.choice(upi_domains)
        amount = round(random.uniform(50, 50000), 2)  # Higher amounts for fraud detection
        status = random.choice(["Success", "Failed", "Pending"])
        category = random.choice(categories)
        is_fraud = 1 if random.random() < 0.07 else 0  # 7% fraud cases

        # If fraudulent, make transaction amount suspiciously high
        if is_fraud:
            amount *= random.uniform(2, 6)
            amount = round(amount, 2)  # Keep decimal format

        data.append([transaction_id, sender, receiver, upi_id, amount, status, category, is_fraud])

    return pd.DataFrame(data, columns=["Transaction_ID", "Sender", "Receiver", "UPI_ID", "Amount", "Status", "Category", "Fraud"])

# Create Dataset
df = generate_fake_data(1000)  # Generate 1000 records
df.to_csv("dataset.csv", index=False)

print("Dataset Generated: dataset.csv with Indian Names and Numeric Transaction IDs")
