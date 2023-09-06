from . import *

# This is the output: {'data': {'question': {'questionId': '1', 'questionFrontendId': '1', 'title': 'Two Sum', 'titleSlug': 'two-sum', 'isPaidOnly': False, 'difficulty': 'Easy', 'likes': 51113, 'dislikes': 1649, 'categoryTitle': 'Algorithms'}}}
# write a dataclass for this
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
        
        return cls(questionId=questionId, questionFrontendId=questionFrontendId, title=title, titleSlug=titleSlug, isPaidOnly=isPaidOnly, difficulty=difficulty, likes=likes, dislikes=dislikes, categoryTitle=categoryTitle)

class questionTitle(QueryTemplate):
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
        query_result = self.leet_API.post_query(self.graphql_query)
        self.result = Question.from_dict(query_result['data'])
    
    def format_table(self):
        table = LeetTable()
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Difficulty')
        table.add_column('categoryTitle')
        
        q = self.result
        
        table.add_row(q.questionFrontendId, q.title, q.difficulty, q.categoryTitle)
        print(table)
        
    def show(self):
        pass
    