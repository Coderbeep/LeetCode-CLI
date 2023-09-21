from leetcode.models import *

@dataclass
class Submission():
    id: int
    title: str
    titleSlug: str
    statusDisplay: str
    runtime: str
    memory: str
    langName: str
    
@dataclass
class questionSubmisstionList(JSONWizard):
    submissions: List[Submission]
    
    @classmethod
    def from_dict(cls, data):
        submissions_data = data['questionSubmissionList']['submissions']
        submissions = [Submission(id=item.get('id'), 
                                  title=item.get('title'), 
                                  titleSlug=item.get('titleSlug'), 
                                  statusDisplay=item.get('statusDisplay'), 
                                  runtime=item.get('runtime'),
                                  memory=item.get('memory'),
                                  langName=item.get('langName')) 
                       for item in submissions_data]
        return cls(submissions=submissions)


class submissionList(QueryTemplate):
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.question_slug = ""
        self.list_view = False
        self.submission_download = False
        
        self.graphql_query = None
        self.result = None  
        self.params = {'offset': 0, 'limit': 20, 'lastKey': None, 'questionSlug': ""}
    
    def parse_args(self, args):
        self.params['questionSlug'] = args.question_slug
        if args.list:
            self.list_view = True
        else:
            self.submission_download = True
        
    def execute(self, args):
        self.parse_args(args)
        
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        self.result = questionSubmisstionList.from_dict(self.result['data'])
        if self.list_view:
            self.show()
        if self.submission_download:
            print(self.get_code())
    
        
    def show(self):
        table = LeetTable()
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Status Display')
        table.add_column('Runtime')
        table.add_column('Memory')
        table.add_column('Language')
        
        submissions = self.result.submissions
        for x in submissions:
            table.add_row(x.id, x.title, x.statusDisplay, x.runtime, x.memory, x.langName)
        print(table)
    
    def get_code(self):
        # TODO: returning the code of the first submission for now
        submission_details = submissionDetails(self.result.submissions[0].id)
        submission_details.execute()
        return submission_details.result.code