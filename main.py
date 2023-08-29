import argparse
from models import *

def main():
    parser = argparse.ArgumentParser(description="Leet CLI")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    stats_parser = subparsers.add_parser("stats", help="Display statistics")
    stats_parser.set_defaults(func=userProblemsSolved)
    
    problems_parser = subparsers.add_parser("problems", help="Display problems")
    problems_parser.add_argument('page', type=int, help='Page number', nargs='?', default=1)
    problems_parser.set_defaults(func=problemsetQuestionList)
    
    group = problems_parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--solved', action='store_true', help='Display only solved problems.')
    group.add_argument('-t', '--todo', action='store_true', help='Display only to do.')
    group.add_argument('-a', '--attempted', action='store_true', help='Display only attempted problems.')
    
    today_problem_parser = subparsers.add_parser('today', help="Display today's problem.")
    today_problem_parser.set_defaults(func=questionOfToday)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        command_instance = args.func()
        command_instance.execute(args)
    else:
        print("Unknown command. Use 'leet --help' for available commands.")

    
if __name__ == '__main__':
    main()