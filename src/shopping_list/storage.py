''' Ops/Functions for load/save'''

import json
import os
from decimal import Decimal, InvalidOperation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FILE = os.path.join(BASE_DIR, "shopping.json")
PRICE_FILE = os.path.join(BASE_DIR, "prices.json")

# Loading JSON files

def load_list():
    '''Loads or creates JSON file for list'''
    if not os.path.exists(STORAGE_FILE):
        return []
    
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
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

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
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
    os.makedirs(os.path.dirname(STORAGE_FILE) or ".", exist_ok=True)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)
   

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




