from typing import List
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from tabulate import tabulate
from graphql_query import GraphQLQuery
from template import QueryTemplate

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
        self.params = {'categorySlug': "", 'skip': 0, 'limit': 5, 'filters': {'status': "AC"}}
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)

    def execute(self, args):
        self.show()
        
    def show(self):
        result_object = QueryResult.from_dict(self.result['data'])
        
        data = {}
        
        for item in result_object.questions:
            data[item.frontendQuestionId] = [item.title, item.status, item.difficulty]
        
        table_data = [[id] + attributes for id, attributes in data.items()]
        
        print(tabulate(table_data, 
                    headers=['ID', 'Title', 'Status', 'Difficulty'], 
                    tablefmt='psql'))