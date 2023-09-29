from datetime import datetime, timedelta

from leetcode.models import *


# TODO: Add the submission ID into the table, so that the user can copy paste that to download the submitted code
@dataclass
class MatchedUser:
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
    
    problemsSolvedBeatsStats: List[DifficultyPercentage]
    submitStatsGlobal: Dict[str, List[DifficultySubmission]]

@dataclass
class QueryResult(JSONWizard):
    @dataclass
    class DifficultyCount:
        difficulty: str
        count: int
    
    allQuestionsCount: List[DifficultyCount] # questions count according to difficulty
    matchedUser: MatchedUser
    
class UserProblemsSolved(QueryTemplate):
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
                if 'errors' in self.result:
                    raise Exception(self.result['errors'][0]['message'])
                self.result = QueryResult.from_dict(self.result['data'])
            self.show()
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
        self.recent_submissions()
    
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
        console.print(table)

    @staticmethod
    def time_ago(timestamp: int) -> str:
        current_time = datetime.now()
        timestamp_time = datetime.fromtimestamp(timestamp)
        time_difference = current_time - timestamp_time

        if time_difference < timedelta(minutes=1):
            return "just now"
        elif time_difference < timedelta(hours=1):
            minutes = time_difference.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_difference < timedelta(days=1):
            hours = time_difference.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif time_difference < timedelta(weeks=1):
            days = time_difference.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = time_difference.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"

    def recent_submissions(self):
        with Loader('Fetching recent submissions...', ''):
            self.submissions_query = self.parser.extract_query('recentAcSubmissions')
            self.subm_params = {'username': self.params['username'], 'limit': 10}
            self.subm_result = self.leet_API.post_query(GraphQLQuery(self.submissions_query, self.subm_params))
            self.subm_result = self.subm_result['data']['recentAcSubmissionList']

            self.id_query = self.parser.extract_query('GetQuestionId')
            
            table = LeetTable(title='Recent Submissions', width = 70)
            table.add_column('ID')
            table.add_column('Title')
            table.add_column('Time')
            
            for subm in self.subm_result:
                self.subm_params = {'titleSlug': subm['titleSlug']}
                question_id = self.leet_API.post_query(GraphQLQuery(self.id_query, self.subm_params))['data']['question']['questionId']
                table.add_row(question_id, subm['title'], self.time_ago(int(subm['timestamp'])))

        print(table)
        

# if __name__ == '__main__':
    # from argparse import Namespace
    # user = UserProblemsSolved()
    # user.execute(Namespace(username='skygragon'))
    # result = user.result
    # question_counts = [x.count for x in result.allQuestionsCount][1:]
    
    # submit_counts = []
    # for diff, subm in result.matchedUser.submitStatsGlobal.items():
    #     for submission in subm:
    #         submit_counts.append(submission.count)
    # submit_counts = submit_counts[1:]
    
    # bars = []
    # for x, y in zip(question_counts, submit_counts):
    #     bar = styles.CustomBar(end=(y/x) * 100)
    #     bars.append(bar)
        
    # result = user.recent_submissions()
    # result = result['data']['recentAcSubmissionList']
    
    # table = LeetTable(title='Recent Submissions', width = 50)
    # table.add_column('ID')
    # table.add_column('Title')
    # table.add_column('Time')
    
    # for subm in result:
    #     question_id = GetQuestionDetail(subm['titleSlug']).question_id
    #     table.add_row(question_id, subm['title'], time_ago(int(subm['timestamp'])))
        
    # left_container = rich.containers.Renderables(bars)
    # right_container = rich.containers.Renderables([table])
    
    # columns = rich.columns.Columns([left_container, right_container], column_first=True)
    # console.print(columns)