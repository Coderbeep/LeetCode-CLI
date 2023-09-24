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
class QuestionSubmisstionList(JSONWizard):
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



# TODO: Emojis/colors for status display (Accepted, Wrong Answer, Runtime Error)
# TODO: Handle empty submissions table
class SubmissionList(QueryTemplate):
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.question_id: int = None
        self.show_terminal = False
        self.submission_download = False
        
        self.graphql_query = None
        self.result = None  
        self.params = {'offset': 0, 'limit': 20, 'lastKey': None, 'questionSlug': None}
    
    def parse_args(self, args):
        self.question_id = args.id
        self.params['questionSlug'] = ProblemInfo.get_title_slug(self.question_id)
        
        if getattr(args, 'show'):
            self.show_terminal = True
            
        if getattr(args, 'download'):
            self.submission_download = True
        
    def execute(self, args):
        try:
            with Loader('Fetching submission list...', ''):
                self.parse_args(args)
                self.graphql_query = GraphQLQuery(self.query, self.params)
                self.result = self.leet_API.post_query(self.graphql_query)
                self.result = QuestionSubmisstionList.from_dict(self.result['data'])
                if not self.result.submissions:
                    raise ValueError("Apparently you don't have any submissions for this problem.")
            self.show()
            
            if self.show_terminal:
                self.show_code()

            if self.submission_download:
                self.download_submission()
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
        
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
        console.print(table)
        
    
    @staticmethod
    def fetch_accepted(submissions):
        return next((x for x in submissions if x.statusDisplay == 'Accepted'), None)
    
    def show_code(self):
        try:
            with Loader('Fetching latest accepted code...', ''):
                acc_submission = self.fetch_accepted(self.result.submissions)
                
                if not acc_submission:
                    raise ValueError("No accepted submissions found.")
                
                submission_id = acc_submission.id
                
                query = self.parser.extract_query('SubmissionDetails')
                params = {'submissionId': submission_id}
                graphql_query = GraphQLQuery(query, params)
                result = self.leet_API.post_query(graphql_query)
                
                code = result['data']['submissionDetails']['code']
                
            console.print(rich.rule.Rule('Latest accepted code', style='bold blue'), width=100)
            console.print(rich.syntax.Syntax(code, 'python', theme='monokai', line_numbers=True), width=100)
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
        
    def download_submission(self):
        try:
            with Loader('Downloading latest accepted code...', ''):
                acc_submission = self.fetch_accepted(self.result.submissions)
            
                if not acc_submission:
                    raise ValueError("No accepted submissions found.")

                query = self.parser.extract_query('SubmissionDetails')
                params = {'submissionId': acc_submission.id}
                graphql_query = GraphQLQuery(query, params)
                result = self.leet_API.post_query(graphql_query)
                
                code = result['data']['submissionDetails']['code']
                file_name = f"{acc_submission.titleSlug}.{acc_submission.id}.py"
                with open(file_name, 'w') as file:
                    file.write(code)
                    
            console.print(f"File saved as {file_name}")
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            
        
        