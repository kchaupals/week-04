''' Ops/Functions for load/save'''
# Standart library
import os
import json
import platform
import csv
import subprocess
from datetime import datetime
from decimal import Decimal, InvalidOperation
# Local modules
import utils

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)
LISTS_DIR = os.path.join(BASE_DIR, "lists")
os.makedirs(LISTS_DIR, exist_ok=True)

# Prices file is used for all lists that exists
PRICE_FILE = os.path.join(BASE_DIR, "prices.json")

# By default using shopping.json in base dir
default_list_file = os.path.join(BASE_DIR, "shopping.json")
active_list_file = default_list_file

# Getting active list and etc

def set_active_list(list_name: str):
    '''Switch active shopping list'''
    global active_list_file

    # If 'default' use shopping.json in base dir
    if list_name.lower() == "default":
        active_list_file = default_list_file
        if not os.path.exists(active_list_file):
            with open(active_list_file, "w", encoding="utf-8") as f:
                json.dump([], f)
    else:
        # Any other list goes to lists/ folder
        active_list_file = os.path.join(LISTS_DIR, f"{list_name}.json")
        if not os.path.exists(active_list_file):
            with open(active_list_file, "w", encoding="utf-8") as f:
                json.dump([], f)
def save_list(items):
    with open(active_list_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)           

def get_active_list_name():
    name = os.path.basename(active_list_file).replace(".json", "")
    if active_list_file == default_list_file:
        return "default"
    return name

# Loading JSON files

def load_list():
    '''Loads or creates JSON file for list'''
    if not os.path.exists(active_list_file):
        return []
    
    try:
        with open(active_list_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠ JSON corrupted. Resetting file.")
        return []
    
def load_prices():
    '''Loads or creates JSON file for prices'''
    if not os.path.exists(PRICE_FILE):
        return {}
    
    try:
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠ JSON corrupted. Resetting file.")
        return {}

# Adding items to JSON files

def add_item(item, qty):
    '''Fn to add item to list / Validate for duplicates'''
    storage = load_list()
    temp_item = item.strip().lower()

    for existing in storage:
        if existing["item"].lower() == temp_item:
            existing["qty"] += int(qty)
            break
    else:
        storage.append({
            "item": item.capitalize(),
            "qty": int(qty),
        })

    with open(active_list_file, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)

def save_prices(prices):
    '''Saves prices to library'''
    with open(PRICE_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=2, ensure_ascii=False)

def get_items():
    '''Returns all items from list'''
    return load_list()

def get_price(item):
    prices = load_prices()
    if not prices:
        return None
    return prices.get(item.strip().lower())

def set_price(item, price):
    prices = load_prices()
    prices[item.strip().lower()] = str(price)
    save_prices(prices)   

def list_total():
    '''Returns total value of items added to list'''
    storage = load_list()
    prices = load_prices()
        
    if not storage:
        print("The list is empty, add item to get total amount")
        return Decimal("0.00")
    
    listTotal = Decimal("0.00")

    for item in storage:
        try:
            name = item["item"].lower()
            qty = int(item["qty"])

            price = Decimal(prices.get(name, "0"))
            lineTotal = price * qty
            listTotal += lineTotal
        except (InvalidOperation, TypeError):
            print("Invalid values on shopping list")
            continue

        total = listTotal.quantize(Decimal("0.01"))
    return total


def clear_list():
    '''Clears all entries on list'''
    os.makedirs(os.path.dirname(active_list_file) or ".", exist_ok=True)
    with open(active_list_file, "w", encoding="utf-8") as f:
        json.dump([], f)

# Export list options

def export_list(file_type="csv", filename=None):
    '''Export the current shopping list to CSV or text'''
    items = load_list()
    prices = load_prices()

    if not items:
        print("❌ Nothing to export. List is empty")
        return
    
    # Creating timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if filename:
        base_name = filename
    else:
        base_name = get_active_list_name()
    
    full_filename = f"{base_name}_{timestamp}.{file_type}"
    full_path = os.path.join(EXPORT_DIR, full_filename)

    # ------------ CSV ------------
    if file_type == "csv":
        with open(full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Item", "Quantity", "Price per unit", "Line Total"])
            for item in items:
                name = item["item"]
                qty = int(item.get("qty", 0))
                price = Decimal(prices.get(name.lower(), "0")) 
                line_total = utils.calc_line_total(item)
                writer.writerow([name, qty, f"{price:.2f}", f"{line_total:.2f}"])

    # ------------ TXT ------------
    elif file_type == "txt":
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"Shopping List: {base_name}\n")
            f.write(f"Exported: {timestamp}\n")
            f.write("-"* 50 + "\n")
            total = Decimal("0.00")
            for idx, item in enumerate(items, start=1):
                name = item["item"]
                qty = int(item.get("qty", 0))
                price = Decimal(prices.get(name.lower(), "0"))
                line_total = utils.calc_line_total(item)
                total += line_total
                f.write(f"{idx}. {name:<7} x {qty:>3} - {price:>4} EUR/piece = {line_total:>3} EUR\n")
            f.write("-"* 50 + "\n")
            f.write(f"Total: {total:.2f} EUR\n")

    else:
        print("❌ Unsupported file type. Use <csv> or <txt>.\n")
        return
    print(f"✅ Exported to {full_path}")

    # ------------ Auto Open Exported file ------------
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(full_path)
        elif system == "Darwin": # macOS
            subprocess.run(["open", full_path])
        else: # Linux
            subprocess.run(["xdg-open", full_path])
    except Exception:
        print("⚠ Could not automatically open the file.")


# Input validation 

def validate_args(item, qty, price):
    """Validate and convert add command arguments."""

    if not item or not item.strip():
        raise ValueError("Item name cannot be empty")
    
    try:
        qty = int(qty)
        if qty <= 0:
            raise ValueError("Quantity must be a positive integer")
    except ValueError:
        raise ValueError(f"Invalid quantity '{qty}' - must be a positive integer")
    
    try:
        price = Decimal(price)
        if price <= 0:
            raise ValueError("Price must be positive")
    except:
        raise ValueError(f"Invalid price '{price}' - must be a valid number")
    
    return item.strip(), qty, price




