#!/usr/bin/python
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from GQL_parse import Parser
import argparse
from tabulate import tabulate
import os

""" Global variables declaration """
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUERIES = os.path.join(SCRIPT_DIR, 'queries.graphql')
URL = 'https://leetcode.com/graphql/'

""" Connects to the API's endpoint with a query and returns 
    the answer given by the server."""
def query_leet(query, params):
    # State the API endpoint for communicationm
    transport = AIOHTTPTransport(url=URL)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query, variable_values=params)
    return result
    
def handle_statistics(args):
    parser = Parser(QUERIES)
    query_names = parser.extract_query_names()
    query = parser.extract_query(query_names[0])
    params = {'username': 'coderbeep'}
    result = query_leet(query, params)

    # If the amount of exercises done is too low, the percentage
    # tab is not filled, so we only initialize it with None values
    table_data = {
        'Difficulty': [stats['difficulty'] for stats in result['matchedUser']['submitStatsGlobal']['acSubmissionNum']],
        'Count': [submission['count'] for submission in result['matchedUser']['submitStatsGlobal']['acSubmissionNum']],
        'Percentage': [None] * len(result['matchedUser']['submitStatsGlobal']['acSubmissionNum'])  # Initialize with None values
    }

    # Update 'Percentage' based on difficulty
    percentage_dict = {stats['difficulty']: stats['percentage'] for stats in result['matchedUser']['problemsSolvedBeatsStats']}
    for i, difficulty in enumerate(table_data['Difficulty']):
        if difficulty in percentage_dict:
            table_data['Percentage'][i] = percentage_dict[difficulty]
        if table_data['Percentage'][i] is None:
            table_data['Percentage'][i] = 'n/a'
        
    print(tabulate(table_data, headers='keys', tablefmt='psql', stralign='right'))
    
def handle_problems(args):
    parser = Parser(QUERIES)
    query_names = parser.extract_query_names()
    query = parser.extract_query(query_names[1])
    params = {'categorySlug': "", 'skip': 80, 'limit': 20, 'filters': {}}
    result = query_leet(query, params)

    titles = [question['title'] for question in result['problemsetQuestionList']['questions']]
    for title in titles:
        print(title)

def main():
    parser = argparse.ArgumentParser(description="Leet CLI")

    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    stats_parser = subparsers.add_parser("stats", help="Display statistics")
    stats_parser.set_defaults(func=handle_statistics)
    
    problems_parser = subparsers.add_parser("problems", help="Display problems")
    problems_parser.set_defaults(func=handle_problems)
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print("Unknown command. Use 'leet --help' for available commands.")

    
if __name__ == '__main__':
    main()