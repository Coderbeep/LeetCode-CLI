from dataclass_wizard.type_def import JSONObject
from GQL_parse import Parser, query_leet, QUERIES_PATH
from tabulate import tabulate
from dataclasses import dataclass
from typing import List, Dict, Optional, Type
from dataclass_wizard import JSONWizard

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

def handle_problems():
    # Extract the query for problems
    parser = Parser(QUERIES_PATH)
    query_names = parser.extract_query_names()
    query = parser.extract_query(query_names[1])
    params = {'categorySlug': "", 'skip': 0, 'limit': 5, 'filters': {}}
    result = query_leet(query, params)

    result_object = QueryResult.from_dict(result)
    
    data = {}
    
    for item in result_object.questions:
        data[item.frontendQuestionId] = [item.title, item.status, item.difficulty]
    
    table_data = [[id] + attributes for id, attributes in data.items()]
    
    print(tabulate(table_data, 
                   headers=['ID', 'Title', 'Status', 'Difficulty'], 
                   tablefmt='psql'))
    

        
if __name__ == '__main__':
    handle_problems()