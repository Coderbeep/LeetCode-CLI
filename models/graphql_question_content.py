from . import *

class questionContent(QueryTemplate):
    def __init__(self, titleSlug):
        super().__init__()
        self.params = {'titleSlug': titleSlug}
        self.result = None
        
        self.execute()
        self.question_panels = LeetQuestionToSections(self.result)
        
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)['data']['question']['content']
    
    def __repr__(self):
        for x in self.question_panels:
            print(x)
        return ''