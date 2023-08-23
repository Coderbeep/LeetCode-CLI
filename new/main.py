import argparse
from skill_stats import userProblemsSolved
from problems_list import problemsetQuestionList


QUERIES = {'userProblemsSolved': 0,
           'problemsetQuestionList': 1}


def main():

    # params = {'categorySlug': "", 'skip': 0, 'limit': 5, 'filters': {'status': "AC"}}

    # configuration = Configuration(SESSION)
    # leet_api = LeetAPI(configuration)
    
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