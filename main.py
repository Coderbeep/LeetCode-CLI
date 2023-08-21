from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://leetcode.com/graphql/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=False)

# read the query from 'queries.graphql' file and then put username parameter to jakubkubiak234 and execute the query
with open('query.graphql', 'r', encoding='utf-8') as file:
    query = gql(file.read())
    # params = {"username": "jakubkubiak234"}
    params = {'categorySlug': "", 'skip': 0, 'limit': 50, 'filters': {}}

    result = client.execute(query, variable_values=params)
    print(result)
    