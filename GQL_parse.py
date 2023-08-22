import re
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os

""" Global variables declaration """
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUERIES_PATH = os.path.join(SCRIPT_DIR, 'queries.graphql')
URL = 'https://leetcode.com/graphql/'
class Parser():
    def __init__(self, filename):
        self.filename = filename
    
    def extract_query_names(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            query_names = []
            for line in file:
                if line.startswith('query '):
                    query_name = re.split(r'[(|)]', line)[0].split(' ')[1]
                    query_names.append(query_name)
        return query_names
    
    def extract_query(self, query_name):
        with open(self.filename, 'r', encoding='utf-8') as file:
            query = ''
            for line in file:
                if line.startswith('query ' + query_name):
                    query += line
                    break
            for line in file:
                if line.startswith('}'):
                    query += line
                    break
                query += line
        return gql(query)

def query_leet(query, params):
    # State the API endpoint for communicationm
    transport = AIOHTTPTransport(url=URL)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query, variable_values=params)
    return result