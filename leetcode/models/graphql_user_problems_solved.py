from leetcode.models import *
import sys

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
        self.params = {'username': ''}
        self.graphql_query = None
        self.result = None
        
        
    def parse_args(self, args):
        if getattr(args, 'username'):
            self.params['username'] = getattr(args, 'username')
        else:
            username = self.config.user_config.get('username')
            if username:
                self.params['username'] = self.config.user_config.get('username')
            else:
                console.print("Username neither provided nor configured. Head to --help.", style=ALERT)
                sys.exit(1)
        
    def execute(self, args):
        try:
            with Loader('Fetching user stats...', ''):            
                self.parse_args(args)
                
                self.graphql_query = GraphQLQuery(self.query, self.params)
                self.result = self.leet_API.post_query(self.graphql_query)
                if self.result['errors']:
                    raise Exception(self.result['errors'][0]['message'])
                self.result = QueryResult.from_dict(self.result['data'])
            self.show()
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
    
    def show(self):
        difficulties = [x.difficulty for x in self.result.allQuestionsCount]
        question_counts = [x.count for x in self.result.allQuestionsCount]
        beaten_stats = [x.percentage for x in self.result.matchedUser.problemsSolvedBeatsStats]
        beaten_stats.insert(0, None)
        submit_counts = []
        for diff, subm in self.result.matchedUser.submitStatsGlobal.items():
            for submission in subm:
                submit_counts.append(submission.count)
        
        table = LeetTable(title=self.params['username'] + "'s Leetcode Stats")
        table.add_column('Difficulty')
        table.add_column('Question Count')
        table.add_column('Beaten Stats (%)')
        table.add_column('Submit Count')
        
        for diff, count, stats, subm in zip(difficulties, question_counts, beaten_stats, submit_counts):
            table.add_row(diff, str(count), str(stats), str(subm)) 
        print(table)

    
    