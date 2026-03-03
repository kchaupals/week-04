''' Main CLI'''
import storage
import argparse

def print_help():
    help_text = '''
    Shopping List

    Usage:
        shop.py list
        shop.py add "<item>" "<price>"
        shop.py total
        shop.py clear

    Commands:
        list                 Shows current shopping list
        add <item> <price>   Add item with price to shopping list
        total                Shows total sum of items on shopping list
        clear                Clears current shopping list

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
        '''Shows shopping list'''
        storage.list_output()
    elif cmd == "add":
        if len(cmd_args) != 3:
            print_help()
            return
        item, qty, price = cmd_args
        storage.add_item(item, qty, price)
    elif cmd == "total":
        total, count, listQty = storage.list_total()
        print(f"Total ammount {total} EUR ({listQty} pieces, {count} items)\n")
    elif cmd == "clear":
        storage.clear_list()
    else:
        print_help()


if __name__ == "__main__":
    main()