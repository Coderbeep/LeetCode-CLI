from leetcode.models import *
from leetcode.models.graphql_question_content import QuestionContent
from leetcode.models.graphql_question_info_table import QuestionInfoTable


@dataclass
class Question():
    difficulty: str
    status: str
    title: str
    titleSlug: str
    frontendQuestionId: int

@dataclass
class QueryResult(JSONWizard):
    date: str
    userStatus: str
    link: str
    question: Question
    
    @classmethod
    def from_dict(cls, data):
        date = data['activeDailyCodingChallengeQuestion']['date']
        userStatus = data['activeDailyCodingChallengeQuestion']['userStatus']
        link = data['activeDailyCodingChallengeQuestion']['link']
        
        
        question = data['activeDailyCodingChallengeQuestion']['question']
        question = Question(title=question.get('title'),
                             status=question.get('status'),
                             titleSlug=question.get('titleSlug'),
                             difficulty=question.get('difficulty'),
                             frontendQuestionId=question.get('frontendQuestionId'))
        
        return cls(date=date, userStatus=userStatus, link=link, question=question)  

class QuestionOfToday(QueryTemplate):
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.contentFlag = False
        self.browserFlag = False
        self.title_slug: str = None
        
        self.params = {}
        self.graphql_query = None
        self.result = None
        
    def parse_args(self, args):
        if getattr(args, 'browser'): 
            self.browserFlag = True
        if getattr(args, 'contents'):
            self.contentFlag = True
    
    def execute(self, args):
        with Loader('Fetching question of the day...', ''):
            self.parse_args(args)
            
            self.graphql_query = GraphQLQuery(self.query, self.params)
            self.result = self.leet_API.post_query(self.graphql_query)
            self.result = QueryResult.from_dict(self.result['data'])
            self.title_slug = self.result.question.titleSlug
        self.show()
    
    
    def show(self):
        question_info_table = QuestionInfoTable(self.title_slug)
        if self.contentFlag:
            print(question_info_table)
            print()
            with Loader('Fetching question content...', ''):
                question_content = QuestionContent(self.title_slug)
            print(question_content)
        elif self.browserFlag:
            print(question_info_table)
            link = self.config.host + self.result.link
            print(f'Link to the problem: {link}')
            self.open_in_browser(link)
        else:
            print(question_info_table)


        
    
