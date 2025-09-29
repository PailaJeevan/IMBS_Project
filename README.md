# 📦 Inventory Management & Billing System -- Python Console Application

## 🎯 Objective

A simple yet powerful console-based **Python application** that manages
product inventory, processes customer orders, and generates bills.\
This project demonstrates **inventory control, billing, and reporting**
using only the **Python Standard Library** --- no third-party packages
required!

------------------------------------------------------------------------

## 🗂️ Project Structure

    ├── main.py                 # Entry point for the application
    ├── inventory_backend.py    # Core logic: Product, Inventory & Order management
    ├── inventory_frontend.py   # User interface (menus, inputs, outputs)
    ├── inventory.csv           # Product inventory data (auto-created)
    ├── sales_records.csv       # Sales history (auto-created)
    ├── bills/                  # Directory for generated bills
    └── data/                   # Directory for storing related files

------------------------------------------------------------------------

## ✨ Features at a Glance

✔️ Add, update, search & delete products
✔️ Manage customer orders with stock validation
✔️ Auto-update stock after purchase
✔️ Apply discounts to orders (optional)
✔️ Generate clean text-based bills (`.txt` / `.csv`)
✔️ Track daily sales performance
✔️ Monitor low-stock products

------------------------------------------------------------------------

# 📋 Requirements

This project uses only the **Python Standard Library**.  
No external dependencies are required.  

## 🛠️ Runtime Requirement
- Python **3.7+**

---

If you want to list requirements in a file, create a `requirements.txt`:

    # requirements.txt
    python>=3.7

------------------------------------------------------------------------

## 🚀 How to Run

Clone this repository and run the application:

``` bash
git clone https://github.com/your-username/inventory-billing-system.git
cd inventory-billing-system
python main.py
```

Follow the interactive **menu-driven interface** for product management,
order processing, and report generation.

------------------------------------------------------------------------

## 🧾 Sample Workflow

1.  **Add Products** → Add items to inventory
2.  **Create Order** → Add items to cart → Confirm purchase
3.  **Generate Bill** → Option to save as `.txt` or `.csv`
4.  **Check Reports** → View sales and low-stock alerts

------------------------------------------------------------------------

## 📊 Example Bill

    === INVOICE ===
    Order ID: 20250929174530
    Date: 2025-09-29 17:45:30

    Items Purchased:
    ----------------------------------------
    Laptop (P101) - 2 x 50000.00 = 100000.00
    Mouse (P102)  - 3 x 500.00   = 1500.00
    ----------------------------------------
    TOTAL: 101500.00

    Thank you for your purchase!
    ========================================

------------------------------------------------------------------------

## 📖 About the Modules

### 🔹 Product Management

This module allows the admin to manage inventory efficiently.
Functions include:
- Adding new products with ID, name, price, and stock quantity
- Updating existing product details
- Deleting products no longer available
- Searching by ID or name
- Viewing all available products in the inventory

### 🔹 Order Processing

This module handles customer purchases.
Functions include:
- Adding products to a cart with quantity validation
- Removing items from the cart
- Calculating totals with optional discounts
- Auto-updating stock once the order is processed

### 🔹 Billing

After order confirmation, a **bill/invoice** is generated.
- Includes Order ID, Date/Time, Item details, and Total amount
- Option to save bill in `.txt` or `.csv` format
- Stored under the `bills/` directory for future reference

### 🔹 Reports

The system can generate business insights with:
- **Daily Sales Report** → Orders, items sold, and total sales amount
- **Low Stock Report** → Products below a specified threshold

------------------------------------------------------------------------

## ✅ Key Deliverables

-   Inventory CRUD operations
-   Order management & billing system
-   Report generation (sales & stock)
-   File-based persistence with CSV
-   Console-based user interface

------------------------------------------------------------------------

## 📩 Contact

- 👨‍💻 **Developer:** Paila Jeevan
- 📧 **Email:** pailajeevan21@gmail.com
- 🌐 **GitHub:**
https://github.com/PailaJeevan

💡 Feel free to fork, contribute, or drop a message if you have ideas to
improve this project!
