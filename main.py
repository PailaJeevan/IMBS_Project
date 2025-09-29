#!/usr/bin/env python3
"""
Inventory Management & Billing System - Main Entry Point
"""

from inventory_frontend import InventoryApp
import os
import sys

def ensure_data_directories():
    """Create required directories if they don't exist"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('bills', exist_ok=True)

def displaying_welcome():
    """Show welcome message and system information"""
    print("\n" + "=" * 50)
    print("INVENTORY MANAGEMENT & BILLING SYSTEM".center(50))
    print("=" * 50)
    print(f"Python {sys.version.split()[0]}".center(50))
    print("=" * 50 + "\n")

def main():
    # Initialize system requirements
    ensure_data_directories()
    displaying_welcome()
    
    # Start the application
    try:
        app = InventoryApp()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nError starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()