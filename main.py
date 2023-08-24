import argparse
from models import *

def main():
    parser = argparse.ArgumentParser(description="Leet CLI")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    stats_parser = subparsers.add_parser("stats", help="Display statistics")
    stats_parser.set_defaults(func=userProblemsSolved)
    
    problems_parser = subparsers.add_parser("problems", help="Display problems")
    problems_parser.set_defaults(func=problemsetQuestionList)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        command_instance = args.func()
        command_instance.execute(args)
    else:
        print("Unknown command. Use 'leet --help' for available commands.")

    
if __name__ == '__main__':
    main()