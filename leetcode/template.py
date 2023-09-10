from leetcode.GQL_parse import Parser
from leetcode.configuration import Configuration
from leetcode.leet_api import LeetAPI
import os

class QueryTemplate():
    def __init__(self):
        self.config = Configuration()
        self.leet_API = LeetAPI(self.config)
        self.parser = Parser()
        
        self.params = None
        
        self.query_name = None
        
        self.query = None
        
        self.get_name()
        self.get_query()
    
    def show(self):
        """ Basic information showing functionality. """
        pass
    
    def get_name(self):
        self.query_name = self.__class__.__name__

    def get_query(self):
        self.query = self.parser.extract_query(self.query_name)

    def execute(self):
        """ Method to handle the args passed by the 
            argument parser. """
        pass

    def open_in_browser(self, link):
        """ Method to open the question in browser. """
        os.system(f'explorer {link}')
        pass