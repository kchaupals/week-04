''' Utility functions for calculations and command handlers '''

from decimal import Decimal, InvalidOperation
import storage

# Task functions calc_line_total; calc_grand_total and count_units

def calc_line_total(item):
    '''Calculates line total as qty x price'''
    if not item:
        raise ValueError("Item cannot be empty")
    try:
        qty = int(item.get('qty', 0))
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        name = item.get('item')
        if not name:
            raise ValueError("Item name is missing")
        
        price_str = storage.get_price(name)
        if not price_str:
            raise ValueError(f"No price found for '{name}'")
        
        price = Decimal(price_str)
        if price <= 0:
            raise ValueError("Price must be positive")

        return qty * price
    except KeyError as e:
        raise ValueError(f"Item missing required field: {e}")
    except (InvalidOperation, ValueError, TypeError) as e:
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
    '''Displays shopping list with line totals and prices'''
    items = storage.get_items()
    prices = storage.load_prices()

    if not items:
        print("\n📋 Shopping List is empty. \n")
        return
    print("\n📋 Shopping List")
    print("-" * 50)

    for idx, item in enumerate(items, start=1):
        name = item.get("item", 0)
        qty = int(item.get("qty", 0))

        try:
            line_total = calc_line_total(item)
            price = Decimal(storage.get_price(name))            
            print(f"{idx: >3}. {name: <7} x {qty: >3} - {price: >4} EUR/piece = {line_total: >3} EUR")
        except (InvalidOperation, TypeError) as e:
            print(f"⚠️  Error displaying item {idx:>3}. {name:<7} x {qty:>3}: ⚠ {e}")

    print("-" * 50)
    print(f"🛒 Total shopping list value: {storage.list_total()} EUR\n")

def handle_add(item, qty):
    '''Add item to shopping list'''
    try:
        # Validate args (price is temp, will be set later)
        item, qty, _ = storage.validate_args(item, qty, 1) 

        # Get saved price from library
        saved_price = storage.get_price(item)

        # Determine price
        if saved_price:
            choice = input(
                f"Price found:{saved_price} EUR/piece\n [U]se / [C]hange?"
            ).strip().lower()

            if choice == "u":
                price = Decimal(saved_price)
            else:
                while True:
                    try:
                        price_input = input(f"Enter new price for {item.capitalize()}: ")
                        price = Decimal(price_input)
                        print(f"Price updated: {item.capitalize()} ({Decimal(price_input)} EUR)")
                        if price <= 0:
                            raise ValueError
                        break
                    except (InvalidOperation, ValueError):
                        print("❌ Invalid price. Enter a positive number.")
                storage.set_price(item,price)
        else:
            while True:
                try:
                    price_input = input(f"No price found for {item.capitalize()} \n Enter price: ")
                    price = Decimal(price_input)
                    print(f"Price added: {item.capitalize()} ({Decimal(price_input)} EUR)")
                    if price <= 0:
                        raise ValueError
                    break
                except (InvalidOperation, ValueError):
                    print("❌ Invalid price. Enter a positive number.")
            storage.set_price(item, price)
        
        # Add item to shopping list
        storage.add_item(item, qty)

        # Calculate line total 
        line_total = price * qty
        
        # Output
        print(f"✅ Added {item.capitalize()} x {qty} - ({price} EUR/piece) = {line_total} EUR")

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
        total = storage.list_total()
        count = len(items)
        list_qty = count_units(items)
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
    🛒 Shopping List CLI

    Usage:
        python shop.py [-l LIST] <command> [args]
        python shop.py -l EXAMPLE add <item> <qty>
        python shop.py add <item> <quantity>
        python shop.py total
        python shop.py clear

    Commands:
        list                            Shows current shopping list
        add <item> <quantity>           Add item to shopping list
        total                           Shows total sum of items on shopping list
        clear                           Clears current shopping list

    Options:
        -l, --list                      Choose shopping lists (default uses shopping.json)
        -h, --help                      Show this help message and exit
'''
    print(help_text)