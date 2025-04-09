import streamlit as st
import Backend as bd
import pandas as pd
from datetime import datetime

# Streamlit App Title
st.set_page_config(page_title="Warehouse Management System", layout="wide")
st.title("📦 Warehouse Management System")

def show_table(results):
    if results:
        df = pd.DataFrame(results, columns=["Product ID", "Name", "Quantity", "Price"])  
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

# Tabs for different functionalities
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📥 Add Product", "❌ Remove Product", "✏️ Modify Product",
    "⚠️ Low Stock", "🔍 Search Product", "💲 Sort by Price", "📋 View All Products" 
])

# Function to show success and error messages with styling
def show_message(status, message):
    if status:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

# Low Stock Alert Function
def check_low_stock():
    try:
        low_stock_items = bd.get_low_stock(10)  # Fetch products below threshold (default = 10)
        alerts = []  

        for item in low_stock_items:
            product_id, name, quantity, _ = item  # Unpacking (product_id, product_name, quantity, price)
            alert = f"🚨 {product_id} ({name}) has only {quantity} units left!"
            if quantity == 0:
                alert = f"❌ {product_id} ({name}) is OUT OF STOCK!"
            alerts.append(alert)

        return alerts

    except Exception as e:
        return [f"Error fetching low stock items: {str(e)}"]

# Display Low Stock Alerts at the Top
low_stock_alerts = check_low_stock()
for alert in low_stock_alerts:
    st.warning(alert)

# Tab 1: Add Product
with tab1:
    st.header("Add New Product")
    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price", min_value=0.01, step=0.01)
    
    
    if st.button("Add Product", use_container_width=True):
        try:
            if name and quantity>1 and price>0.01 :
                bd.add_product(name, quantity, price)
                show_message(True, "Product added successfully!")
        except Exception as e:
            show_message(False, f"Error: {str(e)}")

# Tab 2: Remove Product
with tab2:
    st.header("Remove Product")
    product_id = st.number_input("Product ID", min_value=1, step=1)
    
    if st.button("Remove Product", use_container_width=True):
        try:
            if bd.search_product(product_id)==[] :
                show_message(False,"No such product available")
            else:
                bd.remove_product(product_id)
                show_message(True, "Product removed successfully!")
        except Exception as e:
            show_message(False, f"Error: {str(e)}")

# Tab 3: Modify Product
with tab3:
    st.header("Modify Product")
    product_id = st.number_input("Product ID to Modify", min_value=1, step=1)
    new_name = st.text_input("New Product Name")
    new_quantity = st.number_input("New Quantity", min_value=1, step=1)
    new_price = st.number_input("New Price", min_value=0.01, step=0.01)

    if st.button("Update Product", use_container_width=True):
        try:
            if bd.search_product(product_id)==[] :
                show_message(False,"No such product available")
            else :
                bd.update_product(product_id, new_name, new_quantity, new_price)
                show_message(True, "Product updated successfully!")

                updated_product = bd.search_product(product_id)
                if updated_product:
                    product = updated_product[0]  
                    st.write(f"**🆔 Product ID:** {product[0]}")
                    st.write(f"**📛 Name:** {product[1]}")
                    st.write(f"**📦 Quantity:** {product[2]}")
                    st.write(f"**💲 Price:** {product[3]}")

        except Exception as e:
            show_message(False, f"Error: {str(e)}")

# Tab 4: Low Stock Products with Detailed Alerts

# Tab 4: Low Stock Products with Pop-Up Alerts
with tab4:
    st.header("⚠️ Low Stock Products")
    
    threshold = st.number_input("Stock Threshold", min_value=1, value=10, step=1)
    
    if st.button("Check Low Stock", use_container_width=True):
        try:
            low_stock_items = bd.get_low_stock(threshold)  
            
            if low_stock_items:
                alerts = []  

                for item in low_stock_items:
                    product_id, name, quantity, _ = item  
                    alert_message = f"🚨 {product_id} ({name}) has only {quantity} units left!"
                    
                    if quantity == 0:
                        alert_message = f"❌ {product_id} ({name}) is OUT OF STOCK!"

                    alerts.append(alert_message)

                
                # JavaScript alert for pop-up
                js_alert = f"""
                <script>
                    alert("{alerts[0]}");
                </script>
                """
                st.markdown(js_alert, unsafe_allow_html=True)

                # Toast Notification (Streamlit)
                for alert in alerts:
                    st.toast(alert, icon="⚠️")

                show_table(low_stock_items)

            else:
                st.info("🎉 No products are low on stock!")

        except Exception as e:
            show_message(False, f"Error: {str(e)}")


# Tab 5: Search Product
with tab5:
    st.header("Search Product")
    search_term = st.number_input("Enter product id to search", min_value=1, step=1, format="%d")

    if st.button("Search", use_container_width=True):
        try:
            results = bd.search_product(search_term)
            if results:
                if results:
                    product = results[0]  # Only one product is searched at a time
                    st.write(f"**🆔 Product ID:** {product[0]}")
                    st.write(f"**📛 Name:** {product[1]}")
                    st.write(f"**📦 Quantity:** {product[2]}")
                    st.write(f"**💲 Price:** {product[3]}")
            else:
                st.warning("🔍 No matching products found!")
        except Exception as e:
            show_message(False, f"Error: {str(e)}")

# Tab 6: Sort Products by Price
with tab6:
    st.header("Sort Products by Price")
    order = st.radio("Sort Order", ["Ascending", "Descending"], horizontal=True)

    if st.button("Sort Products", use_container_width=True):
        try:
            sorted_products = bd.sort_products("ASC" if order == "Ascending" else "DESC")
            if sorted_products:
                show_table(sorted_products)
            else:
                st.warning("📉 No products found!")
        except Exception as e:
            show_message(False, f"Error: {str(e)}")

# Tab 7: View All Products
with tab7:
    st.header("All Products in Inventory")

    if st.button("View the inventory", use_container_width=True):
        try:
            all_products = bd.fetch_all_products()
            if all_products:
                show_table(all_products)
            else:
                st.warning("📦 No products available!")
        except Exception as e:
            show_message(False, f"Error: {str(e)}")