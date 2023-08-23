from typing import Any
import requests
from GQL_parse import Parser

SESSION = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNTEwMTA2MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwYTkyYmQ4NjZjNDM4OTk5OTdmOWRhNmRjYTM0MTViODM3NzM3YzciLCJpZCI6NTEwMTA2MCwiZW1haWwiOiJqYWt1Ymt1YmlhazIzNEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImNvZGVyYmVlcCIsInVzZXJfc2x1ZyI6ImNvZGVyYmVlcCIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9qYWt1Ymt1YmlhazIzNC9hdmF0YXJfMTYzNDU3MDE0NS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2OTI3MjkwNjYsImlwIjoiMmEwMToxMWJmOjYxMDo2YjAwOmM4MzE6NmRhMDpiNTJlOjc2M2IiLCJpZGVudGl0eSI6ImVhZjNhNmYyNTU3YzM2NzQwODJlZDc1NDNiN2ZlMDMzIiwic2Vzc2lvbl9pZCI6NDQ2OTQ5MzQsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.n-Hiqw4iUUTWTHZHTGyNjuuaUewk5CZKuRBlRkRLxcs'     

class Configuration():
    def __init__(self, session_id: str):
        self.host = 'https://leetcode.com/'
        self.session_id = session_id
        
        self._csrf_cookie: str = None
        
        self._headers: dict = {'x-csrftoken': self.csrf_cookie,
                               'Referer': self.host}
        self._cookies: dict = {'csrftoken': self.csrf_cookie,
                               'LEETCODE_SESSION': self.session_id}       
    
    @property
    def csrf_cookie(self) -> str:
        response = requests.get(url=self.host,
                                cookies={"LEETCODE_SESSION": self.session_id})
        return response.cookies["csrftoken"]
    
    @csrf_cookie.setter
    def csrf_cookie(self, value: str):
        self._csrf_cookie = value
        
    @property
    def headers(self) -> dict:
        return self._headers
    
    @property
    def cookies(self) -> dict:
        return self._cookies
   
class GraphQLQuery():
    types = ['query', 'variables']
    
    def __init__(self, query: str = None, variables: dict = None):
        self._query = query
        self._variables = variables

    @property
    def query(self):
        return self._query
    
    @query.setter
    def query(self, value: str):
        self._query = value
        
    @property
    def variables(self):
        return self._variables
    
    @variables.setter
    def variables(self, value: dict):
        self._variables = value
        
    def to_dict(self) -> dict:
        result = {}
        
        for item_type in self.types:
            if getattr(self, item_type) is None:
                raise ValueError(f"GraphQLQuery.{item_type} is None")
            result[item_type] = getattr(self, item_type)
            
        return result
        
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GraphQLQuery):
            return False
        else:
            return self.query == other.query and self.variables == other.variables

    def __repr__(self) -> str:
        # String implementation for debugging purposes
        return f"GraphQLQuery(query={self.query}, variables={self.variables})"

class LeetAPI():
    def __init__(self, config: Configuration):
        self.config = config

    def post_query(self, query: GraphQLQuery):
        response = requests.post(url="https://leetcode.com/graphql",
                                 headers=self.config.headers,
                                 json=query.to_dict(),
                                 cookies=self.config.cookies)
        return response.json()