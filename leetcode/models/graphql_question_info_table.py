from leetcode.models import *

@dataclass
class Question():
    questionId: str
    questionFrontendId: str
    title: str
    titleSlug: str
    isPaidOnly: bool
    difficulty: str
    likes: int
    dislikes: int
    categoryTitle: str
    status: str
    
    @classmethod
    def from_dict(cls, data):
        questionId = data['question']['questionId']
        questionFrontendId = data['question']['questionFrontendId']
        title = data['question']['title']
        titleSlug = data['question']['titleSlug']
        isPaidOnly = data['question']['isPaidOnly']
        difficulty = data['question']['difficulty']
        likes = data['question']['likes']
        dislikes = data['question']['dislikes']
        categoryTitle = data['question']['categoryTitle']
        status = data['question']['status']
        
        return cls(questionId=questionId, questionFrontendId=questionFrontendId, title=title, titleSlug=titleSlug, isPaidOnly=isPaidOnly, difficulty=difficulty, likes=likes, dislikes=dislikes, categoryTitle=categoryTitle, status=status)

class QuestionInfoTable(QueryTemplate):
    def __init__(self, titleSlug: str = None):
        super().__init__()
        self.params = {'titleSlug': titleSlug}
        self.graphql_query = None
        self.result = None
        
        self.table: LeetTable = None
        
        self.execute()
        self.format_table()
    
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        self.result = Question.from_dict(self.result['data'])
    
    def format_table(self):
        self.table = LeetTable()
        self.table.add_column('ID')
        self.table.add_column('Title')
        self.table.add_column('Difficulty')
        self.table.add_column('Status')
        self.table.add_column('categoryTitle')
        
        q = self.result
        
        self.table.add_row(q.questionId, q.title, q.difficulty, q.status, q.categoryTitle)
        
    def show(self):
        console.print(self.table)
    
    def __rich_console__(self, console: Console, options):
        return self.table.__rich_console__(console, options)
    