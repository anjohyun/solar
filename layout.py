import requests
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

# Your existing code to call the API
api_key = os.getenv("up_BBuHWnUU9XAXW9jKJxNqMgiNZtCjL")  # Replace with your API key
filename = "receipts/receipt3.jpeg"  # Replace with any other document
model = "receipt-extraction"  # Replace with any other model

url = "https://api.upstage.ai/v1/document-ai/extraction"
headers = {"Authorization": f"Bearer {api_key}"}
files = {"document": open(filename, "rb")}
data = {"model": model}
response = requests.post(url, headers=headers, files=files, data=data)

# Parse the JSON response
extracted_data = response.json()
print(extracted_data)  # Print to inspect the JSON structure

# Initialize variables for receipt and items data
merchant_name = None
branch_name = None
store_address = None
store_phone = None
payment_method = None
total_amount = None
subtotal = None
tax_rate = None
tax_amount = None
items = []

# Extract relevant information
for field in extracted_data['fields']:
    key = field['key']
    value = field['refinedValue']

    if key == 'store.store_name':
        merchant_name = value
    elif key == 'store.branch_name':
        branch_name = value
    elif key == 'store.store_address':
        store_address = value
    elif key == 'store.store_phone_number':
        store_phone = value
    elif key == 'transaction.cc_code':
        payment_method = value
    elif key == 'total.charged_price':
        total_amount = value.replace('$', '')
    elif key == 'total.subtotal_price' and field['type'] == 'content':
        subtotal = value.replace('$', '')
    elif key == 'total.tax_rate':
        tax_rate = value
    elif key == 'total.tax_price':
        tax_amount = value.replace('$', '')
    elif field['type'] == 'group':  # Look for groups which might contain items
        # Extract the item details
        item_name = None
        item_price = None

        for prop in field['properties']:
            if 'menu.product_name' in prop['key']:
                item_name = prop['refinedValue']
            elif 'menu.unit_product_total_price_before_discount' in prop['key']:
                item_price = prop['refinedValue']

        if item_name and item_price:
            items.append({'product_name': item_name, 'price': item_price})

print(items)
# Set up the database connection
conn = sqlite3.connect('receipt.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY,
    merchant_name TEXT,
    branch_name TEXT,
    store_address TEXT,
    store_phone TEXT,
    payment_method TEXT,
    subtotal REAL,
    tax_rate TEXT,
    tax_amount REAL,
    total_amount REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    receipt_id INTEGER,
    product_name TEXT,
    price REAL,
    FOREIGN KEY (receipt_id) REFERENCES receipts (id)
)
''')

# Insert the receipt data
cursor.execute('''
INSERT INTO receipts (merchant_name, branch_name, store_address, store_phone, payment_method, subtotal, tax_rate, tax_amount, total_amount)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (merchant_name, branch_name, store_address, store_phone, payment_method, subtotal, tax_rate, tax_amount, total_amount))

receipt_id = cursor.lastrowid  # Get the id of the inserted receipt

# Insert the items data
for item in items:
    product_name = item.get('product_name')
    price = item.get('price')
    
    cursor.execute('''
    INSERT INTO items (receipt_id, product_name, price)
    VALUES (?, ?, ?)
    ''', (receipt_id, product_name, price))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted into the database successfully.")
