import re
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os

""" Global variables declaration """
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUERIES_PATH = os.path.join(SCRIPT_DIR, 'queries.graphql')
URL = 'https://leetcode.com/graphql/'
class Parser():
    def __init__(self, filename = QUERIES_PATH):
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
        return query

def query_leet(query, params):
    # State the API endpoint for communicationm
    # q: what are the names of authorization headers for leetcode webstie?
    # a: X-CSRFToken, Cookie
    
    csrf = 'ar8CMs7YTxwrVlgtBn4hSzoBurEv23pPgcQLyZb1Pdgm6UtsGjUIessRS4lzgybr'
    session = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNTEwMTA2MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwYTkyYmQ4NjZjNDM4OTk5OTdmOWRhNmRjYTM0MTViODM3NzM3YzciLCJpZCI6NTEwMTA2MCwiZW1haWwiOiJqYWt1Ymt1YmlhazIzNEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImNvZGVyYmVlcCIsInVzZXJfc2x1ZyI6ImNvZGVyYmVlcCIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9qYWt1Ymt1YmlhazIzNC9hdmF0YXJfMTYzNDU3MDE0NS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2OTI3MjkwNjYsImlwIjoiMmEwMToxMWJmOjYxMDo2YjAwOmM4MzE6NmRhMDpiNTJlOjc2M2IiLCJpZGVudGl0eSI6ImVhZjNhNmYyNTU3YzM2NzQwODJlZDc1NDNiN2ZlMDMzIiwic2Vzc2lvbl9pZCI6NDQ2OTQ5MzQsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.n-Hiqw4iUUTWTHZHTGyNjuuaUewk5CZKuRBlRkRLxcs'     


    headers = {
        "csrftoken": csrf,
        "LEETCODE_SESSION": session,        
    }
    
    transport = AIOHTTPTransport(url=URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query, variable_values=params)
    return result