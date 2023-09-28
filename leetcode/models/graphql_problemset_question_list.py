from leetcode.models import *

@dataclass
class QueryResult(JSONWizard):
    @dataclass
    class Question():
        title: str
        status: str
        difficulty: str
        frontendQuestionId: int
        questionId: int
    total: int
    questions: List[Question]
    
    @classmethod
    def from_dict(cls, data):
        total = data['problemsetQuestionList']['total']
        questions_data = data['problemsetQuestionList']['questions']
        questions = [
            cls.Question(
                title=item.get('title'),
                status=item.get('status'),
                difficulty=item.get('difficulty'),
                frontendQuestionId=item.get('frontendQuestionId'),
                questionId=item.get('questionId')
            )
            for item in questions_data
        ]
        return cls(total=total, questions=questions)
    
class ProblemTotalCount(QueryTemplate):
    def __init__(self, filters={}):
        super().__init__()
        self.graphql_query = None
        self.result = None
        self.params = {'categorySlug': '', 'filters': filters}
        
        self.execute()
        
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.result['data']['problemsetQuestionList']['total']


class ProblemsetQuestionList(QueryTemplate):
    """ A class to represent a list of LeetCode problems.

    Args:
        filters (dict, optional): Filters to apply to the query. Defaults to {}. 
            - 'difficulty' (str, optional): Difficulty level. Valid values: 'EASY', 'MEDIUM', 'HARD'.
            - 'status' (str, optional): Status of the problem. Valid values: 'NOT_STARTED', 'TRIED', 'AC'.
        limit (int, optional): Maximum number of problems to retrieve. Defaults to None.
        skip (int, optional): Number of problems to skip. Defaults to 0.
    """

    def __init__(self, filters={}, limit=None, skip=0):
        super().__init__()

        # Instance specific variables
        self.page : int = 1
        self.max_page : int = 0
        self.filters = filters
        self.limit = limit or self.config.user_config.get('question_list_limit')
        self.skip = skip
        
        self.params = {'categorySlug': "", 
                       'skip':self.skip, 
                       'limit': self.limit, 
                       'filters': self.filters}
        
        self.graphql_query = None
        self.result = None
        
    def fetch_data(self, parameters: Dict = None) -> QueryResult:
        """ Fetches the data from the LeetCode API.

        Args:
            parameters (dict, optional): Parameters to pass to the query. Defaults to None.

        Returns:
            QueryResult: The result of the query.
        """

        if parameters is None:
            parameters = self.params
        with Loader('Fetching problems...', ''):
            self.graphql_query = GraphQLQuery(self.query, parameters)
            self.result = self.leet_API.post_query(self.graphql_query) # Take the response from the API
            self.result = QueryResult.from_dict(self.result['data'])
        return self.result
        
    def _execute(self, args):
        """ Executes the query with the given arguments and displays the result.

        Args:
            args (argparse.Namespace): The arguments passed to the query.
        """

        self.__parse_args(args)
        self.result = self.fetch_data()
        self.show(self.result)

    def show(self, query_result: Optional[QueryResult] = None) -> None:
        """ Displays the query result in a table.

        Args:
            query_result (QueryResult, optional): The result of the query. Defaults to None.
                If the result is None, the method will try to fetch the data with defauly parameters and than display it.
        """

        if query_result is None:
            query_result = self.fetch_data()
        
        displayed : int = self.limit * self.page if self.limit * self.page < query_result.total else self.result.total
        
        table = LeetTable(title=f'Total number of problems retrieved: {query_result.total}\n',
                            caption=f"Page #{self.page} / ({displayed}/{self.result.total})")
        
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Status')
        table.add_column('Difficulty')
        for item in query_result.questions:
            table.add_row(item.questionId, item.title, item.status, item.difficulty)
        console.print(table)
    
    def __validate_page(self):
        """ Validates the current page number.
        If the number is too large, sets the page number to the last page.
        """

        count = ProblemTotalCount().__call__()
        self.page = min(self.page, -(-count // self.limit))
        self.params['skip'] = self.limit * self.page - self.limit # update the skip value

    def __parse_args(self, args):
        """ Parses the arguments passed to the query.

        Args:
            args (argparse.Namespace): The arguments passed to the query.
        """
        
        # Parse status argument
        status_mapping = {"solved": "AC",
                            "todo": "NOT_STARTED",
                            "attempted": "TRIED"}
        status_argument = None
        for status_arg in status_mapping.keys():
            if getattr(args, status_arg):
                status_argument = status_arg
                break
            
        if status_argument is not None:
            self.params['filters']['status'] = status_mapping[status_argument]
            
        # Parse the page argument
        self.page = getattr(args, 'page') 
        self.params['skip'] = self.limit * self.page - self.limit
        
        self.__validate_page()