from typing import List, Dict, Optional
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from tabulate import tabulate
from from_git import GraphQLQuery
from template import QueryTemplate

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
        data = {}

        # Add allQuestionsCount data
        for item in result_object.allQuestionsCount:
            if item.difficulty not in data:
                data[item.difficulty] = [item.count, None, None]
            else:
                data[item.difficulty][0] = item.count

        # Add problemsSolvedBeatsStats data
        for item in result_object.matchedUser.problemsSolvedBeatsStats:
            if item.difficulty not in data:
                data[item.difficulty] = [None, item.percentage, None]
            else:
                data[item.difficulty][1] = item.percentage

        # Add submitStatsGlobal data
        for difficulty, submissions in result_object.matchedUser.submitStatsGlobal.items():
            for submission in submissions:
                if submission.difficulty not in data:
                    data[submission.difficulty] = [None, None, submission.count]
                else:
                    data[submission.difficulty][2] = submission.count

        # Convert dictionary to list of lists for tabulate
        table_data = [[difficulty] + values for difficulty, values in data.items()]
    
        # Display data with tabulate
        print(tabulate(table_data, 
                    headers=['Difficulty', 'Question Count', 'Beaten Stats %', 'Submit Count'],
                    tablefmt='psql'))

    
    