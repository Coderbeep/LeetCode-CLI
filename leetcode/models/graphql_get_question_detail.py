from leetcode.models import *

class getQuestionDetail(QueryTemplate):
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.question_slug = ""
        
        self.graphql_query = None
        self.result = None
        self.params = {'titleSlug': 'two-sum'}
        
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        print(self.result)
        

instance = getQuestionDetail()
instance.execute()