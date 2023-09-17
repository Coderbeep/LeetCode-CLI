from leetcode.models import *

class getQuestionDetail(QueryTemplate):
    def __init__(self, title_slug: str):
        super().__init__()
        # Instance-specific variables
        self._title_slug = title_slug

        self.graphql_query = None
        self.result = None
        self.params = {'titleSlug': title_slug}

        # Initialize variables to store query data
        self._question_data = None
        self.execute()

    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
        # Store the entire question data
        self._question_data = self.result.get('data', {}).get('question', {})

    @property
    def title_slug(self):
        return self._title_slug

    @property
    def question_id(self):
        return self._question_data.get('questionId')

    @property
    def question_frontend_id(self):
        return self._question_data.get('questionFrontendId')

    @property
    def title(self):
        return self._question_data.get('title')

    @property
    def content(self):
        return self._question_data.get('content')
    
    @property
    def sample_test_case(self):
        return self._question_data.get('sampleTestCase')
