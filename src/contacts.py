'''
Contact List CLI
    
Description: 
    Contact List CLI
    Functions:
        - list: List all contacts
        - add: Add a new contact
        - delete: Delete a contact by index or name
        - search: Search contacts by name or phone number

Modules in use:
    json: JSON (JavaScript Object Notation), specified by RFC 7159 (which obsoletes RFC 4627) and by ECMA-404, is a lightweight data interchange format inspired by JavaScript object literal syntax 
    os: This module provides a portable way of using operating system dependent functionality
    argparse: The argparse module makes it easy to write user-friendly command-line interfaces.
    / Descriptions on modules explored on - https://docs.python.org/ /
    
'''
import json
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(BASE_DIR, "contacts.json")


def load_contacts():
    '''Load contacts from the JSON file.'''
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_contacts(contacts):
    '''Save the list of contacts to the JSON file.'''

    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)


def list_contacts():
    '''Print all contacts in a numbered list.'''
    contacts = load_contacts()

    print("\n📒 Contact List")
    print("-" * 30)

    if not contacts:
        print("No contacts found.")
        return

    for idx, contact in enumerate(contacts, start=1):
        print(f"{idx}. {contact['name']} | {contact['phone']}")


def add_contact(name, phone):
    '''Add a new contact to the list.'''
    contacts = load_contacts()

    if any(c["phone"] == phone for c in contacts):
        print("⚠ Contact with this phone number already exists.")
        return

    contacts.append({
        "name": name,
        "phone": phone
    })

    save_contacts(contacts)
    print(f'✅ Contact {name} ({phone}) added successfully.')


def delete_contact(identifier):
    '''Delete a contact by index or name.'''
    contacts = load_contacts()

    if identifier.isdigit():
        index = int(identifier) - 1
        if 0 <= index < len(contacts):
            removed = contacts.pop(index)
            save_contacts(contacts)
            print(f"🗑 Removed: {removed['name']}")
        else:
            print("Invalid index.")
        return

    updated_contacts = [c for c in contacts if c["name"].lower() != identifier.lower()]

    if len(updated_contacts) == len(contacts):
        print("No contact found with that name.")
        return

    save_contacts(updated_contacts)
    print(f"🗑 Contact '{identifier}' removed.")


def search_contacts(query):
    '''Search contacts by name or phone number.'''

    contacts = load_contacts()
    results = [c for c in contacts if query.lower() in c["name"].lower() or query in c["phone"]]

    print(f"\n🔍 Search results for '{query}':")
    print("-" * 30)

    if not results:
        print("No contacts found.")
        return

    for idx, contact in enumerate(results, start=1):
        print(f"{idx}. {contact['name']} | {contact['phone']}")


def print_help():
    help_text = '''
    📒 Contact List CLI

    Usage:
        contacts.py list
        contacts.py add "<name>" "<phone>"
        contacts.py delete <id|name>
        contacts.py search "<query>"

    Commands:
        list                 List all contacts
        add <name> <phone>   Add a new contact
        delete <id|name>     Delete a contact by index or name
        search <query>       Search contacts by name or phone

    Options:
        -h, --help           Show this help message and exit
'''
    print(help_text)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    parser.add_argument("-h", "--help", action="store_true", help="Show help")

    args = parser.parse_args()

    if args.help or args.command is None:
        print_help()
        return

    cmd = args.command.lower()
    cmd_args = args.args

    if cmd == "list":
        list_contacts()
    elif cmd == "add":
        if len(cmd_args) != 2:
            print_help()
            return
        name, phone = cmd_args
        print(f"Adding {name} | {phone}")
        add_contact(name, phone)
    elif cmd == "delete":
        if len(cmd_args) != 1:
            print_help()
            return
        identifier = cmd_args[0]
        print(f"Deleting {identifier}")
        delete_contact(identifier)
    elif cmd == "search":
        if len(cmd_args) != 1:
            print_help()
            return
        query = cmd_args[0]
        print(f"Searching {query}")
        search_contacts(query)
    else:
        print_help()


if __name__ == "__main__":
    main()