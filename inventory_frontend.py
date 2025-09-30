from inventory_backend import InventoryManager, OrderManager
import datetime
from fpdf import FPDF

class InventoryApp:
    def __init__(self):
        self.inventory_manager = InventoryManager()
        self.order_manager = OrderManager(self.inventory_manager)
        self.run()

    def display_menu(self):
        print("\n=== INVENTORY & BILLING SYSTEM ===")
        print("1. Product Management")
        print("2. Order Processing")
        print("3. Reports")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        return choice

    def product_management_menu(self):
        while True:
            print("\n--- PRODUCT MANAGEMENT ---")
            print("1. Add Product")
            print("2. Update Product")
            print("3. Delete Product")
            print("4. Search Product")
            print("5. View All Products")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.update_product()
            elif choice == '3':
                self.delete_product()
            elif choice == '4':
                self.search_product()
            elif choice == '5':
                self.view_all_products()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def order_processing_menu(self):
        while True:
            print("\n--- ORDER PROCESSING ---")
            print("1. Add Item to Cart")
            print("2. Remove Item from Cart")
            print("3. View Cart")
            print("4. Process Order")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                self.add_to_cart()
            elif choice == '2':
                self.remove_from_cart()
            elif choice == '3':
                self.view_cart()
            elif choice == '4':
                self.process_order()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def reports_menu(self):
        while True:
            print("\n--- REPORTS ---")
            print("1. Daily Sales Report")
            print("2. Low Stock Report")
            print("3. Back to Main Menu")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                self.daily_sales_report()
            elif choice == '2':
                self.low_stock_report()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_product(self):
        print("\n--- ADD NEW PRODUCT ---")
        product_id = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        
        try:
            price = float(input("Enter Product Price: "))
            quantity = int(input("Enter Initial Stock Quantity: "))
        except ValueError:
            print("Invalid input for price or quantity. Please enter numbers.")
            return
        
        if self.inventory_manager.add_product(product_id, name, price, quantity):
            print("Product added successfully!")
        else:
            print("Error: Product with this ID already exists.")

    def update_product(self):
        print("\n--- UPDATE PRODUCT ---")
        product_id = input("Enter Product ID to update: ")
        
        product = self.inventory_manager.search_product(product_id=product_id)
        if not product:
            print("Product not found.")
            return
        
        product = product[0]
        print(f"\nCurrent Details for {product.product_id}:")
        print(f"Name: {product.name}")
        print(f"Price: {product.price:.2f}")
        print(f"Quantity: {product.quantity}")
        
        print("\nEnter new details (leave blank to keep current):")
        name = input(f"Name [{product.name}]: ") or None
        price = input(f"Price [{product.price:.2f}]: ")
        quantity = input(f"Quantity [{product.quantity}]: ")
        
        try:
            price = float(price) if price else None
            quantity = int(quantity) if quantity else None
        except ValueError:
            print("Invalid input for price or quantity. Please enter numbers.")
            return
        
        if self.inventory_manager.update_product(product_id, name, price, quantity):
            print("Product updated successfully!")
        else:
            print("Error updating product.")

    def delete_product(self):
        print("\n--- DELETE PRODUCT ---")
        product_id = input("Enter Product ID to delete: ")
        
        if self.inventory_manager.delete_product(product_id):
            print("Product deleted successfully!")
        else:
            print("Product not found.")

    def search_product(self):
        print("\n--- SEARCH PRODUCT ---")
        print("1. Search by Product ID")
        print("2. Search by Product Name")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            product_id = input("Enter Product ID: ")
            results = self.inventory_manager.search_product(product_id=product_id)
        elif choice == '2':
            name = input("Enter Product Name (or part of name): ")
            results = self.inventory_manager.search_product(name=name)
        else:
            print("Invalid choice.")
            return
        
        if not results:
            print("No products found.")
        else:
            print("\nSearch Results:")
            print("ID\tName\t\tPrice\tStock")
            print("----------------------------------------")
            for product in results:
                print(f"{product.product_id}\t{product.name[:15]}\t{product.price:.2f}\t{product.quantity}")

    def view_all_products(self):
        products = self.inventory_manager.products
        if not products:
            print("No products in inventory.")
            return
        
        print("\n--- ALL PRODUCTS ---")
        print("ID\tName\t\tPrice\tStock")
        print("----------------------------------------")
        for product in products:
            print(f"{product.product_id}\t{product.name[:15]}\t{product.price:.2f}\t{product.quantity}")

    def add_to_cart(self):
        print("\n--- ADD TO CART ---")
        self.view_all_products()
        product_id = input("Enter Product ID to add to cart: ")
        quantity = int(input("Enter Quantity: "))
        
        if self.order_manager.add_to_cart(product_id, quantity):
            print("Item added to cart successfully!")
        else:
            print("Error: Product not found or insufficient stock.")

    def remove_from_cart(self):
        print("\n--- REMOVE FROM CART ---")
        if not self.order_manager.cart:
            print("Cart is empty.")
            return
        
        self.view_cart()
        product_id = input("Enter Product ID to remove from cart: ")
        
        if self.order_manager.remove_from_cart(product_id):
            print("Item removed from cart successfully!")
        else:
            print("Error: Product not found in cart.")

    def view_cart(self):
        cart = self.order_manager.cart
        if not cart:
            print("Cart is empty.")
            return
        
        print("\n--- YOUR CART ---")
        print("Item\t\tQty\tPrice\tSubtotal")
        print("----------------------------------------")
        for item in cart:
            product = item['product']
            print(f"{product.name[:15]}\t{item['quantity']}\t{product.price:.2f}\t{item['subtotal']:.2f}")
        
        total = self.order_manager.calculate_total()
        print("----------------------------------------")
        print(f"TOTAL:\t\t\t\t{total:.2f}")

    def process_order(self):
        if not self.order_manager.cart:
            print("Cart is empty. Add items before processing order.")
            return
        
        self.view_cart()
        apply_discount = input("Apply discount? (y/n): ").lower() == 'y'
        discount = 0
        
        if apply_discount:
            try:
                discount = float(input("Enter discount percentage (0-100): "))
                if discount < 0 or discount > 100:
                    print("Invalid discount. Must be between 0 and 100.")
                    return
            except ValueError:
                print("Invalid discount value. Please enter a number.")
                return
        
        confirm = input("Confirm purchase? (y/n): ").lower()
        if confirm == 'y':
            bill = self.order_manager.process_order(discount)
            print("\n" + bill)
            
            save_bill = input("Save bill to file? (y/n): ").lower()
            if save_bill == 'y':
                filetype = input("Save as (txt/csv): ").lower()
                if filetype not in ['txt', 'csv']:
                    print("Invalid file type. Defaulting to txt.")
                    filetype = 'txt'
                
                filename = self.order_manager.save_bill_to_file(bill, filetype=filetype)
                print(f"Bill saved as {filename}")

    def daily_sales_report(self):
        date_str = input("Enter date for report (YYYY-MM-DD) or leave blank for today: ")
        
        try:
            if date_str:
                date = datetime.datetime.strptime(str(date_str), "%Y-%m-%d").date()
            else:
                date = datetime.date.today()
        except Exception:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        
        report = self.order_manager.get_daily_sales(date)
        
        print(f"\n--- DAILY SALES REPORT FOR {date} ---")
        print(f"Total Orders: {report['num_orders']}")
        print(f"Total Items Sold: {report['total_items']}")
        print(f"Total Sales Amount: {report['total_sales']:.2f}")

        # Automatically save as CSV
        import csv
        csv_filename = f"daily_sales_report_{date}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Total Orders", "Total Items Sold", "Total Sales Amount"])
            writer.writerow([date, report['num_orders'], report['total_items'], f"{report['total_sales']:.2f}"])
        print(f"CSV saved as {csv_filename}")

        # PDF download option removed

    def low_stock_report(self):
        threshold = input("Enter low stock threshold (default 5): ") or "5"
        
        try:
            threshold = int(threshold)
        except ValueError:
            print("Invalid threshold. Using default value 5.")
            threshold = 5
        
        low_stock = self.inventory_manager.get_low_stock_products(threshold)
        
        if not low_stock:
            print(f"\nNo products with stock below {threshold}.")
            return
        
        print(f"\n--- LOW STOCK REPORT (Below {threshold}) ---")
        print("ID\tName\t\tStock")
        print("----------------------------------------")
        for product in low_stock:
            print(f"{product.product_id}\t{product.name[:15]}\t{product.quantity}")

        # Automatically save as CSV
        import csv
        csv_filename = f"low_stock_report_{datetime.date.today()}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Product ID", "Name", "Stock"])
            for product in low_stock:
                writer.writerow([product.product_id, product.name, product.quantity])
        print(f"CSV saved as {csv_filename}")

        # PDF download option removed

    def run(self):
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.product_management_menu()
            elif choice == '2':
                self.order_processing_menu()
            elif choice == '3':
                self.reports_menu()
            elif choice == '4':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = InventoryApp()
