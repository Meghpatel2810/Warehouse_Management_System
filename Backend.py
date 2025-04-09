import mysql.connector

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        # Enter your password
        password=" ",
        database="Pyquest"
    )

# Add a New Product
def add_product(product_name, quantity, price):
    db = connect_db()
    cursor = db.cursor()
    query = "INSERT INTO products (product_name, quantity, price) VALUES (%s, %s, %s)"
    cursor.execute(query, (product_name, quantity, price))
    db.commit()
    print("Product added successfully.")
    cursor.close()
    db.close()

# Remove a Product
def remove_product(product_id):
    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM products WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    db.commit()
    print("Product removed successfully.")
    cursor.close()
    db.close()

# Modify Product Details
def update_product(product_id, product_name, quantity, price):
    db = connect_db()
    cursor = db.cursor()
    query = "UPDATE products SET product_name = %s, quantity = %s, price = %s WHERE product_id = %s"
    cursor.execute(query, (product_name, quantity, price, product_id))
    db.commit()
    print("Product updated successfully.")
    cursor.close()
    db.close()

# Identify Low-Stock Products
def get_low_stock(threshold=10):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM products WHERE quantity < %s"
    cursor.execute(query, (threshold,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Search for a Product by Name
def search_product(search_term):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM products WHERE product_id = %s"
    cursor.execute(query, (search_term,))  # Pass product_id instead of name
    result = cursor.fetchall()
    cursor.close()
    print(result)
    db.close()
    return result

# Sort Products by Price
def sort_products(order="ASC"):
    db = connect_db()
    cursor = db.cursor()
    query = f"SELECT * FROM products ORDER BY price {order}"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Fetch All Products
def fetch_all_products():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result
