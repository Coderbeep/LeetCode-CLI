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
    """ A class to represent a table of question information.
    
    Args:
        titleSlug (str): The title slug of the question to fetch data for.
    """
    
    def __init__(self, titleSlug):
        super().__init__()
        # Instance-specific variables
        self._title_slug = titleSlug
        self._data = None
        self._params = {'titleSlug': titleSlug}
        self._data_fetched: bool = False
        
        self.fetch_data(self.title_slug)
    
    def fetch_data(self, titleSlug: str = None) -> Dict:
        try:
            with Loader('Fetching question details...', ''):
                parameters = self.params
                if titleSlug is None:
                    parameters = self.params
                elif titleSlug != self.title_slug:
                    self.title_slug = titleSlug
                    self.params = {'titleSlug': titleSlug}
                    parameters = self.params
                if self.data_fetched:
                    return self._data

                graphql_query = GraphQLQuery(self.query, parameters)
                response = self.leet_API.post_query(graphql_query)
                if response['data']['question'] is None:
                    raise Exception('There is no question with title slug: ' + titleSlug)
                self.data = Question.from_dict(response['data'])
                self.data_fetched = True
                self.params = parameters
                return self.data
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)
    
    def format_table(self, data: Question):
        """ Formats the given question data into a LeetTable object.

        Args:
            data (Question): The question data to format.

        Returns:
            LeetTable: The formatted table object.
        """
        table = LeetTable()
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Difficulty')
        table.add_column('Status')
        table.add_column('categoryTitle')
        
        table.add_row(data.questionId, 
                        data.title, 
                        data.difficulty, 
                        data.status, 
                        data.categoryTitle)
        
        return table
        
    def show(self):
        """ Displays the question data in a LeetTable. 
        
        If the data has not been fetched yet, an exception is raised.
        """
        if self.data_fetched:
            table = self.format_table(self.data)
            console.print(table)
        else:
            raise Exception("Data is not fetched yet.")
    
    def __rich_console__(self, console: Console, options):
        """ Returns a Rich Table object for console output.

        Raises:
            - Exception: If the data has not been fetched yet.
        """
        if self.data_fetched:
            table = self.format_table(self.data)
            return table.__rich_console__(console, options)
        else:
            raise Exception("Data is not fetched yet.")
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data: dict):
        if data is None:
            raise ValueError(f"Data for question with title slug '{self.title_slug}' is None.")
        self._data = data
        
    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, params: dict):
        self._params = params
        
    @property
    def title_slug(self):
        return self._title_slug
    
    @title_slug.setter
    def title_slug(self, title_slug: str):
        self._title_slug = title_slug
        self._data_fetched = False
        self.params = {'titleSlug': title_slug}
    
    @property
    def data_fetched(self):
        return self._data_fetched
    
    @data_fetched.setter
    def data_fetched(self, data_fetched: bool):
        self._data_fetched = data_fetched
        
if __name__ == "__main__":
    question_table = QuestionInfoTable('two-sum')
    print(question_table)
    
    question_table.fetch_data('add-two-integers')
    print(question_table)