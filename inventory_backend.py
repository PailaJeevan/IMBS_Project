import csv
from datetime import datetime
import os

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

class InventoryManager:
    def __init__(self, filename='inventory.csv'):
        self.filename = filename
        self.products = []
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.products.append(Product(
                        row['product_id'],
                        row['name'],
                        float(row['price']),
                        int(row['quantity'])
                    ))

    def save_inventory(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['product_id', 'name', 'price', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': product.quantity
                })

    def add_product(self, product_id, name, price, quantity):
        if not any(p.product_id == product_id for p in self.products):
            self.products.append(Product(product_id, name, price, quantity))
            self.save_inventory()
            return True
        return False

    def update_product(self, product_id, name=None, price=None, quantity=None):
        for product in self.products:
            if product.product_id == product_id:
                if name is not None:
                    product.name = name
                if price is not None:
                    product.price = price
                if quantity is not None:
                    product.quantity = quantity
                self.save_inventory()
                return True
        return False

    def delete_product(self, product_id):
        for i, product in enumerate(self.products):
            if product.product_id == product_id:
                del self.products[i]
                self.save_inventory()
                return True
        return False

    def search_product(self, product_id=None, name=None):
        results = []
        for product in self.products:
            if (product_id and product.product_id == product_id) or \
               (name and name.lower() in product.name.lower()):
                results.append(product)
        return results

    def get_low_stock_products(self, threshold=5):
        return [p for p in self.products if p.quantity <= threshold]

class OrderManager:
    def __init__(self, inventory_manager):
        self.inventory = inventory_manager
        self.cart = []
        self.sales_records = []
        self.sales_file = 'sales_records.csv'

    def add_to_cart(self, product_id, quantity):
        product = next((p for p in self.inventory.products if p.product_id == product_id), None)
        if product and product.quantity >= quantity:
            self.cart.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            return True
        return False

    def remove_from_cart(self, product_id):
        for i, item in enumerate(self.cart):
            if item['product'].product_id == product_id:
                del self.cart[i]
                return True
        return False

    def calculate_total(self, discount=0):
        total = sum(item['subtotal'] for item in self.cart)
        return total * (1 - discount/100)

    def process_order(self, discount=0):
        if not self.cart:
            return False

        total = self.calculate_total(discount)
        order_time = datetime.now()
        order_id = order_time.strftime("%Y%m%d%H%M%S")

        # Update inventory
        for item in self.cart:
            product = item['product']
            product.quantity -= item['quantity']
        
        self.inventory.save_inventory()

        # Record sale
        sale_record = {
            'order_id': order_id,
            'datetime': order_time,
            'items': len(self.cart),
            'total': total,
            'details': [(item['product'].name, item['quantity'], item['subtotal']) for item in self.cart]
        }
        self.sales_records.append(sale_record)
        self.save_sale_record(sale_record)
        
        # Generate bill
        bill = self.generate_bill(order_id, order_time, total)
        self.cart.clear()
        return bill

    def generate_bill(self, order_id, order_time, total):
        bill_lines = [
            "=== INVOICE ===",
            f"Order ID: {order_id}",
            f"Date: {order_time.strftime('%Y-%m-%d %H:%M:%S')}",
            "\nItems Purchased:",
            "----------------------------------------"
        ]
        
        for item in self.cart:
            product = item['product']
            bill_lines.append(
                f"{product.name} ({product.product_id}) - "
                f"{item['quantity']} x {product.price:.2f} = {item['subtotal']:.2f}"
            )
        
        bill_lines.extend([
            "----------------------------------------",
            f"TOTAL: {total:.2f}",
            "\nThank you for your purchase!",
            "========================================"
        ])
        
        return "\n".join(bill_lines)

    def save_sale_record(self, sale_record):
        file_exists = os.path.exists(self.sales_file)
        with open(self.sales_file, mode='a', newline='') as file:
            fieldnames = ['order_id', 'datetime', 'items', 'total', 'details']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(sale_record)

    def get_daily_sales(self, date=None):
        if not date:
            date = datetime.now().date()
        
        daily_sales = [s for s in self.sales_records 
                      if datetime.strptime(s['datetime'], '%Y-%m-%d %H:%M:%S').date() == date]
        
        total_sales = sum(s['total'] for s in daily_sales)
        total_items = sum(s['items'] for s in daily_sales)
        
        return {
            'date': date,
            'total_sales': total_sales,
            'total_items': total_items,
            'num_orders': len(daily_sales)
        }

    def save_bill_to_file(self, bill_content, filename=None, filetype='txt'):
        if not filename:
            filename = f"bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{filetype}"
        
        with open(filename, 'w') as file:
            file.write(bill_content)
        
        return filename