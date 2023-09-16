from leetcode.models import *
import requests

class sendSubmission(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.graphql_query = None
        self.result = None  
        self.params = {"lang": "python3",
                       "question_id": "88",
                       "typed_code": "class Solution:\n    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:\n        \"\"\"\n        Do not return anything, modify nums1 in-place instead.\n        \"\"\"\n        ",
                       "data_input": "[1,2,3,0,0,0]\n3\n[2,5,6]\n3\n[1]\n1\n[]\n0\n[0]\n0\n[1]\n1"
                        }
    
        self.submit_url = "https://leetcode.com/problems/merge-sorted-array/submit/"
        self.runcode = ''
    
    def execute(self):
        response = requests.post(url="https://leetcode.com/problems/merge-sorted-array/interpret_solution/",
                                    headers=self.config.headers,
                                    json=self.params,
                                    cookies=self.config.cookies)
        self.runcode = response.json()['interpret_id']
            
    def execute_check(self):
        response = requests.get(url=f"https://leetcode.com/submissions/detail/{self.runcode}/check/",
                            headers=self.config.headers,
                            cookies=self.config.cookies)
    
        while response.json().get('state') == 'PENDING' or response.json().get('state') == 'STARTED':
            response = requests.get(url=f"https://leetcode.com/submissions/detail/{self.runcode}/check/",
                                    headers=self.config.headers,
                                    cookies=self.config.cookies)
    
        print(response.json())

subm = sendSubmission()
subm.execute()

subm.execute_check()

# submission_details = submissionDetails(123)
# submission_details.execute()

