import argparse
from user_stats import handle_statistics

""" Command-line Interface implementation """
def main():
    parser = argparse.ArgumentParser(description="Leet CLI")

    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    stats_parser = subparsers.add_parser("stats", help="Display statistics")
    stats_parser.set_defaults(func=handle_statistics)
    
    problems_parser = subparsers.add_parser("problems", help="Display problems")
    problems_parser.set_defaults(func=handle_statistics)
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print("Unknown command. Use 'leet --help' for available commands.")

    
if __name__ == '__main__':
    main()