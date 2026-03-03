''' Ops/Functions for load/save'''

import json
import os
from decimal import Decimal, InvalidOperation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FILE = os.path.join(BASE_DIR, "shopping.json")

def load_list():
    '''Loads or creates JSON file for list'''
    if not os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def add_item(item, qty, price):
    '''Fn to add item to list'''
    storage = load_list()

    storage.append({
        "item": item.capitalize(),
        "qty": int(qty),
        "price": price
    })
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)
    print(f'✅ Added {item.capitalize()} x {qty} - ({price} EUR/piece) = {int(qty) * Decimal(price)} EUR')

def list_output():
    '''Returns list of items and prices'''
    storage = load_list()
    print("\n Shopping List")
    print("-" * 30)

    if not storage:
        print("Shopping List is empty.")
        return
    for idx, item in enumerate(storage, start=1):
        print(f"{'{: >5}'.format(idx)}. {item['item']} x {item['qty']} - {item['price']} EUR/piece = {Decimal(item['price']) * int(item['qty'])} EUR")

def list_total():
    '''Returns total value of items added to list'''
    storage = load_list()
        
    if not storage:
        print("The list is empty, add item to get total amount")
        return Decimal("0.00")
    
    listTotal = Decimal("0.00")
    count = 0
    listQty = 0 
    for item in storage:
        price = item.get("price", 0)
        qty = item.get("qty", 0)
        try:
            listTotal += Decimal(str(price))
            count += 1
            listQty += qty
        except (InvalidOperation, TypeError):
            print("Invalid values on shopping list")
            continue

        total = listTotal.quantize(Decimal("0.01"))
    return total, count, listQty


def clear_list():
    '''Clears all entries on list'''
    try:
        os.makedirs(os.path.dirname(STORAGE_FILE) or ".", exist_ok=True)
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        print("✅ List cleared successfully.")
    except OSError:
        print("❌ Failed to clear the list.")

