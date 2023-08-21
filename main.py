from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from GQL_parse import Parser

FILENAME = 'file.graphql'

def query_leet(query, params):
    # State the API endpoint for communicationm
    transport = AIOHTTPTransport(url="https://leetcode.com/graphql/")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query, variable_values=params)
    return result
    

if __name__ == '__main__':
    parser = Parser(FILENAME)
    query_names = parser.extract_query_names()
    
    query = parser.extract_query(query_names[0])
    params = {'username': 'jakubkubiak234'}
    print(query_leet(query, params))