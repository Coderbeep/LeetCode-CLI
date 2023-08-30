from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from tabulate import tabulate
from graphql_query import GraphQLQuery
from template import QueryTemplate
from rich import print
from content_markdown import LeetQuestionToSections


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

class questionContent(QueryTemplate):
    def __init__(self, titleSlug):
        super().__init__()
        self.params = {'titleSlug': titleSlug}
        self.graphql_query = None
        self.result = None
        self.execute()
    
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)['data']['question']['content']
    

class questionOfToday(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.params = {}
        self.graphql_query = None
        self.result = None
        
        self.contentFlag = False
        self.linkFlag = False
        
    def execute(self, args):
        self.parse_args(args)
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        self.show()
        
    def parse_args(self, args):
        if getattr(args, 'link'): 
            self.linkFlag = True
        if getattr(args, 'contents'):
            self.contentFlag = True
    
    def show(self):
        result_object = QueryResult.from_dict(self.result['data'])
        retranslate = {'ac': 'Solved',
                       'notac': 'Attempted',
                       None: 'Not attempted'}
        
        
        question = result_object.question
        
        table_data = [[question.frontendQuestionId, question.title,
                      retranslate[question.status], question.difficulty]]
        
        print(tabulate(table_data, 
                       headers=['ID', 'Title', 'Status', 'Difficulty'],
                       tablefmt='psql'))
        
        if self.contentFlag:
            titleSlug = result_object.question.titleSlug
            
            question_instance = questionContent(titleSlug)
            html_question = question_instance.result

            question_panels = LeetQuestionToSections(html_question)
            for panel in question_panels:
                print(panel)

        
    
        