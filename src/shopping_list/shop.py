''' Main CLI'''
import storage
import argparse

# Prints argparse info w/ how correctly to use script
print(storage.print_help())

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    parser.add_argument("-h", "--help", action="store_true", help="Show help")

    args = parser.parse_args()

    if args.help or args.command is None:
        storage.print_help()
        return

    cmd = args.command.lower()
    cmd_args = args.args
    try:
        if cmd == "list":
            '''Shows shopping list'''
            storage.list_output()
        elif cmd == "add":
            if len(cmd_args) != 3:
                print("❌ Error: 'add' requires exactly 3 arguments -> <item> <quantity> <price>")
                storage.print_help()
                return
            item, qty, price = storage.validate_args(*cmd_args)
            storage.add_item(item, qty, price)
        elif cmd == "total":
            total, count, listQty = storage.list_total()
            print(f"Total ammount {total} EUR ({listQty} pieces, {count} items)\n")
        elif cmd == "clear":
            storage.clear_list()
        else:
            print(f"❌ Unknown command: '{cmd}'")
            storage.print_help()

    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()