from . import *


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

class questionOfToday(QueryTemplate):
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.contentFlag = False
        self.browserFlag = False
        
        self.params = {}
        self.graphql_query = None
        self.result = None
        
    def execute(self, args):
        with Loader('Fetching question of the day...', ''):
            self.parse_args(args)
            
            self.graphql_query = GraphQLQuery(self.query, self.params)
            self.result = self.leet_API.post_query(self.graphql_query)
            self.result = QueryResult.from_dict(self.result['data'])
        self.show()
        
    def parse_args(self, args):
        if getattr(args, 'browser'): 
            self.browserFlag = True
        if getattr(args, 'contents'):
            self.contentFlag = True
    
    def show_info_table(self):

        question = self.result.question
        
        table = LeetTable()
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Status')
        table.add_column('Difficulty')
        
        table.add_row(question.frontendQuestionId, question.title,
                      question.status, question.difficulty)
        
        print(table)
    
    def show(self):
        if self.contentFlag:
            self.show_info_table()
            print('\n')
            titleSlug = self.result.question.titleSlug
            with Loader('Fetching question content...', ''):
                question_content = questionContent(titleSlug)
            question_content.show()
            
        elif self.browserFlag:
            self.show_info_table()
            link = self.config.host + self.result.link
            print(f'Link to the problem: {link}')
            self.open_in_browser(link)
        else:
            self.show_info_table()

        
    
