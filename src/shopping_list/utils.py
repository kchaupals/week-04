''' Utility functions for calculations and command handlers '''

from decimal import Decimal
import storage

# Task functions calc_line_total; calc_grand_total and count_units

def calc_line_total(item):
    '''Calculates line total as qty x price'''
    if not item:
        raise ValueError("Item cannot be empty")
    try:
        qty = int(item['qty'])
        price = Decimal(item['price'])

        if qty <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive")
        return qty * price
    except KeyError as e:
        raise ValueError(f"Item missing required field: {e}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid item data: {e}")

def calc_grand_total(items):
    '''Calculates all lines total'''
    if not items:
        raise ValueError("Items list cannot be empty")
    
    try:
        total = Decimal('0')
        for item in items:
            total += calc_line_total(item)
        return total
    except ValueError as e:
        raise ValueError(f"Error calculating grand total: {e}")

def count_units(items):
    '''Calculates total quantities in list'''
    if not items:
        raise ValueError("Items list cannot be empty")
    
    try: 
        total_qty = 0
        for item in items:
            total_qty += int(item['qty'])
        return total_qty
    except KeyError as e:
        raise ValueError(f"Item missing required field: {e}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid quantity data: {e}")
    
# Command handlers

def handle_list():
    '''Displays shopping list with line totals'''
    items = storage.get_items()

    if not items:
        print("\n📋 Shopping List is empty. \n")
        return
    print("\n📋 Shopping List")
    print("-" * 50)

    for idx, item in enumerate(items, start=1):
        try:
            line_total = calc_line_total(item)
            print(f"{idx: >3}. {item['item']: <7} x {int(item['qty']): >3} - {item['price']: >4} EUR/piece = {line_total: >3} EUR")
        except ValueError as e:
            print(f"⚠️  Error displaying item {idx}: {e}")

        print("-" * 50)

def handle_add(item, qty, price):
    '''Add item to shopping list'''
    try:
        storage.add_item(item, qty, price)
        temp_item = {
            'item': item.capitalize(),
            'qty': int(qty),
            'price': str(price)
        }
        line_total = calc_line_total(temp_item)
        print(f"✅ Added {item.capitalize()} x {qty} - ({price} EUR/piece) = {line_total} EUR\n")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except OSError as e:
        print(f"❌ File error: {e}")

def handle_total():
    ''''Displays total amount and item count'''
    items = storage.get_items()

    if not items:
        print("\n📋 Shopping List is empty, add items to get total amount \n")
        return
    
    try: 
        total, count, list_qty = storage.list_total()
        print(f"\n Total amount: {total} EUR ({list_qty} pieces, {count} items)\n")
    except ValueError as e:
        print(f"❌ Error: {e}")

def handle_clear():
    '''Clearing the list'''
    try:
        storage.clear_list()
        print("✅ List cleared successfully.\n")
    except OSError as e:
        print(f"❌ File error: {e}")

# Help argparser text

def print_help():
    help_text = '''
    Shopping List

    Usage:
        shop.py list
        shop.py add "<item>" "<quantity>" "<price>"
        shop.py total
        shop.py clear

    Commands:
        list                            Shows current shopping list
        add <item> <quantity> <price>   Add item with price to shopping list
        total                           Shows total sum of items on shopping list
        clear                           Clears current shopping list

    Options:
        -h, --help                      Show this help message and exit
'''
    print(help_text)