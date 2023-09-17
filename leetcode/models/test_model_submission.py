from leetcode.models import *
import requests
import argparse
# TODO: Add a decorator to check if the user is logged in
# TODO: getting code from file
# TODO: getting data input
from graphql_get_question_detail import getQuestionDetail

class sendSubmission(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.submit_url = "https://leetcode.com/problems/merge-sorted-array/submit/"
        self.runcode = ''
    
    def typed_code(self, filename):
        with open(filename, 'r') as file:
            code = file.read()
        return code
            
    def execute_check(self, title_slug, filename):
        question = getQuestionDetail(title_slug)
        self.params = {"lang": "python3",
                       "question_id": question.question_id,
                       "typed_code": self.typed_code(filename),
                       "data_input": question.sample_test_case}
        
        # Interpret solution
        response = requests.post(url=f"https://leetcode.com/problems/{title_slug}/interpret_solution/",
                                 headers=self.config.headers,
                                 json=self.params,
                                 cookies=self.config.cookies)
        runcode = response.json()['interpret_id']
        
        response = requests.get(url=f"https://leetcode.com/submissions/detail/{runcode}/check/",
                            headers=self.config.headers,
                            cookies=self.config.cookies)
    
        while response.json().get('state') == 'STARTED' or response.json().get('state') == 'PENDING':
            response = requests.get(url=f"https://leetcode.com/submissions/detail/{runcode}/check/",
                                    headers=self.config.headers,
                                    cookies=self.config.cookies)
        print(response.json())

submission = sendSubmission()
submission.execute_check('add-two-integers', 'good_solution.py')