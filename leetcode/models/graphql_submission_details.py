from leetcode.models import *

@dataclass
class SubmissionDetails(JSONWizard):
    runtime: str
    memory: str
    code: str
    
    @classmethod
    def from_dict(cls, data):
        data = data['submissionDetails']
        return cls(runtime=data['runtime'], memory=data['memory'], code=data['code'])
    
    
class submissionDetails(QueryTemplate):
    def __init__(self, submission_id) -> None:
        super().__init__()
        # Instance specific variables
        self.submission_id = submission_id
        
        self.graphql_query = None
        self.result = None
        self.params = {'submissionId': self.submission_id}
        
    def execute(self): 
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        self.result = SubmissionDetails.from_dict(self.result['data'])
    
    def show(self):
        print(self.result)
