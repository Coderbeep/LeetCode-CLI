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
        return None
    
    @classmethod
    def get_id(cls, title_slug: str) -> int:
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question__title_slug') == title_slug:
                return item['stat'].get('question_id', 0)
        return None

    def execute(self, args):
        result = self.leet_api.get_request(self.API_URL)
        if getattr(args, 'id'):
            for item in result.get('stat_status_pairs', []):
                if item['stat'].get('question_id') == args.id:
                    self.title_slug = item['stat'].get('question__title_slug', '')
                    break
            if not self.title_slug:
                console.print("Invalid ID has been provided. Please try again.", style=ALERT)
                sys.exit(1)
        elif getattr(args, 'slug'):
            self.title_slug = args.slug
        
        question_info_table = questionInfoTable(self.title_slug)
        question_info_table.show()
        question_content = questionContent(self.title_slug)
        question_content.show()