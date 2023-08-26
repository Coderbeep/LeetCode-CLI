from typing import List
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from tabulate import tabulate
from graphql_query import GraphQLQuery
from template import QueryTemplate
import os 
import keyboard

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


class problemsetQuestionList(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.limit : int = 5
        self.params = {'categorySlug': "", 'skip': 0, 'limit': self.limit, 'filters': {}}
        self.graphql_query = None
        self.result = None
        self.page : int = 1
        self.current_args = None
        
    def move_next(self):
        self.page += 1
        self.params['skip'] += self.limit
        self.execute(self.current_args)
        
    def move_previous(self):
        if self.page > 1:
            self.page -= 1
            self.params['skip'] -= self.limit
            self.execute(self.current_args)
            
    def handle_keyboard_input(self):
        while True:
            key = keyboard.read_event(suppress=True)
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'n':
                    self.move_next()
                elif key.name == 'N':
                    self.move_previous()
            

    def execute(self, args):
        self.current_args = args
        status_mapping = {"solved": "AC",
                          "todo": "NOT_STARTED",
                          "attempted": "TRIED"}
    
        status_argument = next((status_arg for status_arg in status_mapping.keys() if getattr(args, status_arg)), None)
        if status_argument:
            self.params['filters']['status'] = status_mapping[status_argument]
            
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        
        self.show()
        self.handle_keyboard_input()
        
    def show(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        result_object = QueryResult.from_dict(self.result['data'])
        
        data = {}
        
        for item in result_object.questions:
            data[item.frontendQuestionId] = [item.title, item.status, item.difficulty]
        table_data = [[id] + attributes for id, attributes in data.items()]
        
        print(f'Total number of retrieved problems: {result_object.total}\n')
        print(tabulate(table_data, 
                    headers=['ID', 'Title', 'Status', 'Difficulty'], 
                    tablefmt='psql'))
        print(f"Page #{self.page} / ({self.limit * self.page}/{result_object.total})")