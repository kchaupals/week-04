''' Main CLI'''
import argparse
import utils
import storage

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-l", "--list", help="Choose shopping list (default uses shopping.json)", default="default")

    args = parser.parse_args()

    # Sets active list before executing any command 

    storage.set_active_list(args.list)
    active_list_name = storage.get_active_list_name()
    print(f"✅ Using shopping list: {active_list_name}")

    if args.help or args.command is None:
        utils.print_help()
        return

    cmd = args.command.lower()
    cmd_args = args.args

    commands = {
        "list": (utils.handle_list, 0),
        "add": (utils.handle_add, 2),
        "total": (utils.handle_total, 0),
        "clear": (utils.handle_clear, 0),
    }
    
    if cmd not in commands:
        print(f"❌ Unknown command: '{cmd}'\n")
        utils.print_help()
        return
    
    handler, expected_args = commands[cmd]

    if expected_args > 0 and len(cmd_args) != expected_args:
        print(f"❌ Error: '{cmd}' requires exactly {expected_args} arguments\n")
        utils.print_help()
        return
    
    if expected_args > 0:
        handler(*cmd_args)
    else:
        handler()

if __name__ == "__main__":
    main()
