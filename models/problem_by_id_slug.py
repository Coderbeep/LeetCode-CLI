from . import *

class problemByIDSlug(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.api_url = "https://leetcode.com/api/problems/all/"
        self.title_slug: str = None

    def execute(self, args):
        RESULT = self.leet_API.get_request(self.api_url)
        if getattr(args, 'id'):
            for x in RESULT['stat_status_pairs']:
                if x['stat']['question_id'] == args.id:
                    self.title_slug = x['stat']['question__title_slug']
                    break
            if self.title_slug is None:
                console.print("Invalid ID have been provided. Please try again.", style=ALERT)
                sys.exit(1)
        elif getattr(args, 'slug'):
            self.title_slug = args.slug
        
        question_info_table = questionInfoTable(self.title_slug)
        question_info_table.show()
        question_content = questionContent(self.title_slug)
        question_content.show()