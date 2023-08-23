from GQL_parse import Parser
from from_git import Configuration, LeetAPI, GraphQLQuery
SESSION = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNTEwMTA2MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwYTkyYmQ4NjZjNDM4OTk5OTdmOWRhNmRjYTM0MTViODM3NzM3YzciLCJpZCI6NTEwMTA2MCwiZW1haWwiOiJqYWt1Ymt1YmlhazIzNEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImNvZGVyYmVlcCIsInVzZXJfc2x1ZyI6ImNvZGVyYmVlcCIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9qYWt1Ymt1YmlhazIzNC9hdmF0YXJfMTYzNDU3MDE0NS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2OTI3MjkwNjYsImlwIjoiMmEwMToxMWJmOjYxMDo2YjAwOmM4MzE6NmRhMDpiNTJlOjc2M2IiLCJpZGVudGl0eSI6ImVhZjNhNmYyNTU3YzM2NzQwODJlZDc1NDNiN2ZlMDMzIiwic2Vzc2lvbl9pZCI6NDQ2OTQ5MzQsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.n-Hiqw4iUUTWTHZHTGyNjuuaUewk5CZKuRBlRkRLxcs'     

class QueryTemplate():
    def __init__(self):
        self.config = Configuration(SESSION)
        self.leet_API = LeetAPI(self.config)
        self.parser = Parser()
        
        self.params = None
        
        self.query_name = None
        
        self.query = None
        
        self.get_name()
        self.get_query()
    
    def show(self):
        pass
    
    def get_name(self):
        self.query_name = self.__class__.__name__

    def get_query(self):
        self.query = self.parser.extract_query(self.query_name)


