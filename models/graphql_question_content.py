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
        self.result = self.leet_API.post_query(self.graphql_query)
        if 'errors' in self.result:
            print("Cannot find the question with specified title slug. Please try again.")
            sys.exit(1)
        else:
            print(self.result['data']['question'])
            self.result = self.result['data']['question']['content']
    
    def __repr__(self):
        for x in self.question_panels:
            print(x)
        return ''