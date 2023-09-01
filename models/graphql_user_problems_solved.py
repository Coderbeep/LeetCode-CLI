from typing import List, Dict, Optional
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from tabulate import tabulate
from graphql_query import GraphQLQuery
from template import QueryTemplate
from rich import print
from rich.table import Table
import rich
from .styles import LeetTable

@dataclass
class DifficultyCount:
    difficulty: str
    count: int

@dataclass
class DifficultyPercentage:
    # when the leetcode account does not have enough completed exercises
    # the percentage is not calculated, hence the 'Optional' part
    difficulty: str
    percentage: Optional[float]
    
@dataclass
class DifficultySubmission:
    difficulty: str
    count: int

@dataclass
class MatchedUser:
    problemsSolvedBeatsStats: List[DifficultyPercentage]
    submitStatsGlobal: Dict[str, List[DifficultySubmission]]

@dataclass
class QueryResult(JSONWizard):
    allQuestionsCount: List[DifficultyCount] # questions count according to difficulty
    matchedUser: MatchedUser
    
class userProblemsSolved(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.params = {'username': 'coderbeep'}
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        
    def execute(self, args):
        self.show()
    
    def show(self):
        result_object = QueryResult.from_dict(self.result['data'])

        difficulties = [x.difficulty for x in result_object.allQuestionsCount]
        question_counts = [x.count for x in result_object.allQuestionsCount]
        beaten_stats = [x.percentage for x in result_object.matchedUser.problemsSolvedBeatsStats]
        beaten_stats.insert(0, None)
        submit_counts = []
        for diff, subm in result_object.matchedUser.submitStatsGlobal.items():
            for submission in subm:
                submit_counts.append(submission.count)
        
        table = LeetTable(title='coderbeep')
        table.add_column('Difficulty')
        table.add_column('Question Count')
        table.add_column('Beaten Stats (%)')
        table.add_column('Submit Count')
        
        for diff, count, stats, subm in zip(difficulties, question_counts, beaten_stats, submit_counts):
            table.add_row(diff, str(count), str(stats), str(subm)) 
        print(table)

    
    