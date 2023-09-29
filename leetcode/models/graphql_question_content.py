from leetcode.models import *

class QuestionContent(QueryTemplate):
    """ A class to represent a LeetCode problem content. 
    
    Args:
        title_slug (str, optional): The title slug of the problem. If provided the data is fetched when the object is created. Defaults to None."""
    
    def __init__(self, title_slug: str = None):
        super().__init__()
        # Instance-specific variables
        self._title_slug = title_slug
        self._data = None
        self._params = {'titleSlug': title_slug}
        self._data_fetched: bool = False
        
        self.question_panels: List[rich.panel.Panel] = []
        
        if title_slug is not None:
            self.fetch_data(self.title_slug)
        
    def fetch_data(self, title_slug: str = None) -> Dict:
        """ Fetches the content data for the problem.
        
        Args:
            title_slug (str, optional): The title slug of the problem. Defaults to None.
            
        Returns:
            Dict: The content data for the problem.
        """
        try:
            with Loader('Fetching question details...', ''):
                # If provided title slug does not change anything, return the data
                if title_slug is not None and title_slug != self.title_slug:
                    self.title_slug = title_slug

                if self.data_fetched:
                    return self.data

                graphql_query = GraphQLQuery(self.query, self.params)
                response = self.leet_API.post_query(graphql_query)
                
                if response['data']['question'] is None:
                    raise Exception('There is no question with title slug: ' + title_slug)
                
                self.data = response['data']['question']['content']
                self.data_fetched = True
                return self.data
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)
    
    def show(self):
        """ Displays the question panels for the current LeetCode question.

        If the data has not been fetched yet, an exception is raised.
        """
        if self.data_fetched:
            self.question_panels = LeetQuestionToSections(self.data)
            for x in self.question_panels:
                console.print(x)
        else:
            raise Exception("Data is not fetched yet.")
    
    def __rich_console__(self, console: Console, options):
        """ Renders the question content in a rich console.

        If the data has been fetched, the question panels are generated using the LeetQuestionToSections function and yielded.
        If the data has not been fetched, an exception is raised.

        Args:
            console (Console): The console to render the content in.
            options: Additional options for rendering the content.

        Raises:
            Exception: If the data has not been fetched yet.
        """
        if self.data_fetched:
            self.question_panels = LeetQuestionToSections(self.data)
            for x in self.question_panels:
                yield x
        else:
            # raise exception that data is not fetched
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
        
        
if __name__ == '__main__':
    content = QuestionContent('two-sum')
    print(content)
    content.fetch_data('add-two-integers')
    print(content)