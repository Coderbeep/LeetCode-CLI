import argparse
from leetcode.models import *
from leetcode.configuration import check_session_validity, UserConfig

# IDEA: submit the code to the proper question
# using the question slug and question ID that needs to be contained within the filename

# the file can be generated when the user displsays the question

# TODO: questionID and questionFrontendID are not the same
# TODO: handle the wrong cases in the args parser
# TODO: loading ASCII art
# TODO: testing the submission
# TODO: Extend the Details model
# TODO: update the queries file
# TODO: pipes support
# TODO: add a command to open the question in editor
# TODO: add a command to show the solution in the terminal
# TODO: add a command to show the solution in the browser

def positive_integer(value):
    try:
        ivalue = int(value)
        if ivalue > 0:
            return ivalue
        else:
            raise argparse.ArgumentTypeError(f"{value} is not a valid integer")
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

def main():
    parser = argparse.ArgumentParser(description="Leet CLI")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    config_parser = subparsers.add_parser('config', help="Configure the CLI")
    config_parser.add_argument('config_key', type=str, help='Key to change')
    config_parser.add_argument('config_value', type=str, help='Value to set') 
    config_parser.set_defaults(func=UserConfig)
    
    stats_parser = subparsers.add_parser("stats", help="Display statistics")
    stats_parser.add_argument('username', type=str, help='User nickname', nargs='?')
    stats_parser.set_defaults(func=userProblemsSolved)
    
    problems_list_parser = subparsers.add_parser("list", help="Display problem list")
    problems_list_parser.add_argument('page', type=positive_integer, help='Page number', nargs='?', default=1)
    problems_list_parser.set_defaults(func=problemsetQuestionList)
    
    group = problems_list_parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--solved', action='store_true', help='Display only solved problems.')
    group.add_argument('-t', '--todo', action='store_true', help='Display only to do.')
    group.add_argument('-a', '--attempted', action='store_true', help='Display only attempted problems.')
    
    problem_parser = subparsers.add_parser('problem', help="Display problem")
    problem_parser.set_defaults(func=problemInfo)
    group_3 = problem_parser.add_mutually_exclusive_group(required=True)
    group_3.add_argument('-i', '--id', type=positive_integer, help='Problem ID of the problem')
    group_3.add_argument('-s', '--slug', type=str, help='Title slug of the problem.')
    

    today_problem_parser = subparsers.add_parser('today', help="Display today's problem.")
    today_problem_parser.set_defaults(func=questionOfToday)
    
    # submission_parser = subparsers.add_parser('submission', help="Download submission code")
    # submission_parser.add_argument('question_slug', type=str, help='Title slug of the problem.')
    # submission_parser.add_argument('-l', '--list', action='store_true', help='List all submissions.')
    # submission_parser.set_defaults(func=submissionList)
    
    submission_parser = subparsers.add_parser('submit', help='Submit code answer')
    submission_parser.add_argument('question_slug', type=str, help="Title slug of the question")
    submission_parser.add_argument('path', type=str, help='Path to the file with code answer')
    submission_parser.set_defaults(func=sendSubmission)
        
    group_2 = today_problem_parser.add_mutually_exclusive_group()
    group_2.add_argument('-b', '--browser', action='store_true', help='Open the page in browser.')
    group_2.add_argument('-c', '--contents', action='store_true', help='Display contents of the question in the terminal.')
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        command_instance = args.func()
        command_instance.execute(args)
    else:
        print("Unknown command. Use 'leet --help' for available commands.")

    
if __name__ == '__main__':
    if check_session_validity():
        main()