from . import *

class QuestionContent(QueryTemplate):
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
            console.print("Cannot find the question with specified title slug. Please try again.", style=ALERT)
            sys.exit(1)
        else:
            self.result = self.result['data']['question']['content']
    
    def show(self):
        for x in self.question_panels:
            print(x)
    
    def __rich_console__(self, console: Console, options):
        for x in self.question_panels:
            yield x