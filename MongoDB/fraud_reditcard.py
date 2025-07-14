import pandas as pd
from pymongo import MongoClient, errors

# MongoDB Atlas connection string
uri = "mongodb+srv://fakinwande:M50xQRyrwpnBGG9j@cluster0.f8wa06y.mongodb.net/"
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # Attempt to connect and trigger exception if cannot connect
    client.admin.command('ping')
    print("Connected to MongoDB Atlas!")
except errors.ServerSelectionTimeoutError as err:
    print(f"Failed to connect to MongoDB Atlas: {err}")
    exit(1)

db = client['credit_card_db']

# Read the first 50 rows of the CSV
csv_path = 'MongoDB/creditcard.csv'
df = pd.read_csv(csv_path, nrows=50)

# Prepare and insert transactions
transactions = []
transaction_features = []
transaction_status = []
fraud_label_map = {'0': 'Legitimate transaction', '1': 'Fraudulent transaction'}
fraud_label_set = set()

for idx, row in df.iterrows():
    transaction_id = idx + 1
    transactions.append({
        "transaction_id": transaction_id,
        "time_seconds": int(row['Time']),
        "amount": float(row['Amount'])
    })
    features = {f"V{i}": float(row[f"V{i}"]) for i in range(1, 29)}
    features["transaction_id"] = transaction_id
    transaction_features.append(features)
    class_val = bool(row['Class'])
    transaction_status.append({
        "transaction_id": transaction_id,
        "class": class_val
    })
    fraud_label_set.add(row['Class'])

# Insert into MongoDB
if transactions:
    db.transactions.insert_many(transactions)
if transaction_features:
    db.transaction_features.insert_many(transaction_features)
if transaction_status:
    db.transaction_status.insert_many(transaction_status)
if fraud_label_set:
    db.fraud_labels.insert_many([
        {"class": bool(int(cls)), "description": fraud_label_map[str(int(cls))]} for cls in fraud_label_set
    ])

print("Data import complete!") 