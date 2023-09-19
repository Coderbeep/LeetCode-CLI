from leetcode.models import *
from leetcode.configuration import Configuration
from leetcode.leet_api import LeetAPI

class problemInfo():
    API_URL = "https://leetcode.com/api/problems/all/"
    configuration = Configuration()
    leet_api = LeetAPI(configuration)
    
    def __init__(self):
        self.title_slug: str = None

    @classmethod
    def get_title_slug(cls, question_id: int) -> str:
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question_id') == question_id:
                return item['stat'].get('question__title_slug', '')
        else:
            raise ValueError("Invalid ID has been provided. Please try again.")
    
    @classmethod
    def get_id(cls, title_slug: str) -> int:
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question__title_slug') == title_slug:
                return item['stat'].get('question_id', 0)
        else:
            raise ValueError("Invalid slug has been provided. Please try again.")
        
    @classmethod    
    def lookup_slug(cls, question_slug: str): 
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question__title_slug') == question_slug:
                return True
        raise ValueError("Invalid slug has been provided. Please try again.")

    def execute(self, args):
        # TODO: handle the wrong cases in the args parser
        try:
            with Loader('Fetching problem info...', ''):
                result = self.leet_api.get_request(self.API_URL)
                if getattr(args, 'id'):
                    for item in result.get('stat_status_pairs', []):
                        if item['stat'].get('question_id') == args.id:
                            self.title_slug = item['stat'].get('question__title_slug', '')
                            break
                    if not self.title_slug:
                        raise ValueError("Invalid ID has been provided. Please try again.")
                elif getattr(args, 'slug'):
                    for item in result.get('stat_status_pairs', []):
                        if item['stat'].get('question__title_slug') == args.slug:
                            self.title_slug = item['stat'].get('question__title_slug', '')
                            break
                    if not self.title_slug:
                        raise ValueError("Invalid slug has been provided. Please try again.")
            self.show()
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
        
    
    def show(self):
        # TODO: make the __repr__ method for this class
        question_info_table = questionInfoTable(self.title_slug)
        question_info_table.show()
        question_content = questionContent(self.title_slug)
        question_content.show()