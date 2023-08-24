from configuration import Configuration
from graphql_query import GraphQLQuery
import requests

class LeetAPI():
    def __init__(self, config: Configuration):
        self.config = config

    def post_query(self, query: GraphQLQuery):
        response = requests.post(url="https://leetcode.com/graphql",
                                 headers=self.config.headers,
                                 json=query.to_dict(),
                                 cookies=self.config.cookies)
        return response.json()