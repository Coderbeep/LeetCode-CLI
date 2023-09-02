from typing import Any, List
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from tabulate import tabulate
from graphql_query import GraphQLQuery
from template import QueryTemplate
from rich import print
from .styles import LeetTable

# TODO: restrict the page number
@dataclass
class Question():
    title: str
    status: str
    difficulty: str
    frontendQuestionId: int

@dataclass
class QueryResult(JSONWizard):
    total: int
    questions: List[Question]
    
    @classmethod
    def from_dict(cls, data):
        total = data['problemsetQuestionList']['total']
        questions_data = data['problemsetQuestionList']['questions']
        questions = [
            Question(
                title=item.get('title'),
                status=item.get('status'),
                difficulty=item.get('difficulty'),
                frontendQuestionId=item.get('frontendQuestionId')
            )
            for item in questions_data
        ]
        return cls(total=total, questions=questions)

@dataclass
class TotalCount(JSONWizard):
    total: int
class problemTotalCount(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.graphql_query = None
        self.result = None
        self.params = {'categorySlug': "", 'skip': 0, 'limit': 10, 'filters': {}}
        
        self.execute()
        
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.result['data']['problemsetQuestionList']['total']
    

class problemsetQuestionList(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.limit : int = 10
        self.params = {'categorySlug': "", 'skip': 0, 'limit': self.limit, 'filters': {}}
        self.graphql_query = None
        self.result = None
        self.page : int = 1
        self.max_page : int = 0
                
    def parse_args(self, args):
        # Parse status argument
        status_mapping = {"solved": "AC",
                          "todo": "NOT_STARTED",
                          "attempted": "TRIED"}
        status_argument = None
        for status_arg in status_mapping.keys():
            if getattr(args, status_arg):
                status_argument = status_arg
                break
            
        if status_argument is not None:
            self.params['filters']['status'] = status_mapping[status_argument]
            
        # Parse the page argument
        self.page = getattr(args, 'page') 
        self.params['skip'] = self.limit * self.page - self.limit

    def execute(self, args):
        self.parse_args(args)
        
        self.validate_page()
        
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        self.result = QueryResult.from_dict(self.result['data'])

        self.show()
        
    def validate_page(self):
        count = problemTotalCount().__call__()
        if self.page > -(-count // self.limit): # ceil(total / limit)
            self.page = -(-count // self.limit)
            self.params['skip'] = self.limit * self.page - self.limit # update the skip value
        
    def show(self):
        retranslate = {'ac': 'Solved',
                       'notac': 'Attempted',
                       None: 'Not attempted'}
        
        displayed : int = self.limit * self.page if self.limit * self.page < self.result.total else self.result.total
        
        
        table = LeetTable(title=f'Total number of problems retrieved: {self.result.total}\n',
                            caption=f"Page #{self.page} / ({displayed}/{self.result.total})")
        
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Status')
        table.add_column('Difficulty')
        for item in self.result.questions:
            table.add_row(item.frontendQuestionId, item.title, retranslate[item.status], item.difficulty)
        print(table)