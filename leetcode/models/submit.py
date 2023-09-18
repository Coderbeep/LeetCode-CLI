from leetcode.models import *
import requests
import argparse
# TODO: Add a decorator to check if the user is logged in

# Example output of check/ for the success
# {
#     'status_code': 10,
#     'lang': 'python3',
#     'run_success': True,
#     'status_runtime': '55 ms',
#     'memory': 16192000,
#     'code_answer': ['17'],
#     'code_output': [],
#     'std_output_list': ['', ''],
#     'elapsed_time': 80,
#     'task_finish_time': 1694963199341,
#     'task_name': 'judger.runcodetask.RunCode',
#     'expected_status_code': 10,
#     'expected_lang': 'cpp',
#     'expected_run_success': True,
#     'expected_status_runtime': '2',
#     'expected_memory': 6320000,
#     'expected_code_answer': ['17'],
#     'expected_code_output': [],
#     'expected_std_output_list': ['', ''],
#     'expected_elapsed_time': 28,
#     'expected_task_finish_time': 1694963186294,
#     'expected_task_name': 'judger.interprettask.Interpret',
#     'correct_answer': True,
#     'compare_result': '1',
#     'total_correct': 1,
#     'total_testcases': 1,
#     'runtime_percentile': None,
#     'status_memory': '16.2 MB',
#     'memory_percentile': None,
#     'pretty_lang': 'Python3',
#     'submission_id': 'runcode_1694963196.974743_YxDfV90vWl',
#     'status_msg': 'Accepted',
#     'state': 'SUCCESS'
# }


# Example output for bad solution:
# {
#     'status_code': 10,
#     'lang': 'python3',
#     'run_success': True,
#     'status_runtime': '83 ms',
#     'memory': 16188000,
#     'code_answer': ['7'],
#     'code_output': [],
#     'std_output_list': ['', ''],
#     'elapsed_time': 127,
#     'task_finish_time': 1694963261441,
#     'task_name': 'judger.runcodetask.RunCode',
#     'expected_status_code': 10,
#     'expected_lang': 'cpp',
#     'expected_run_success': True,
#     'expected_status_runtime': '2',
#     'expected_memory': 6320000,
#     'expected_code_answer': ['17'],
#     'expected_code_output': [],
#     'expected_std_output_list': ['', ''],
#     'expected_elapsed_time': 28,
#     'expected_task_finish_time': 1694963186294,
#     'expected_task_name': 'judger.interprettask.Interpret',
#     'correct_answer': False,
#     'compare_result': '0',
#     'total_correct': 0,
#     'total_testcases': 1,
#     'runtime_percentile': None,
#     'status_memory': '16.2 MB',
#     'memory_percentile': None,
#     'pretty_lang': 'Python3',
#     'submission_id': 'runcode_1694963259.010116_9rFoEtJQM0',
#     'status_msg': 'Accepted',
#     'state': 'SUCCESS'
# }
class sendSubmission(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.title_slug = None
        self.path = None
        self.runcode = None
        self.submission_id = None

    @property
    def submit_url(self):
        return f"https://leetcode.com/problems/{self.title_slug}/submit/"
    
    @property
    def submit_check_url(self):
        return f"https://leetcode.com/submissions/detail/{self.submission_id}/check/"
    
    @property
    def interpret_url(self):
        return f"https://leetcode.com/problems/{self.title_slug}/interpret_solution/"
    
    @property
    def runcode_check_url(self):
        return f"https://leetcode.com/submissions/detail/{self.runcode}/check/"
    
    def parse_args(self, args):
        pass
        
    def execute(self, args):
        self.title_slug = args.question_slug
        self.path = args.path
        
        self.execute_submission(self.title_slug, self.path)
    
    def load_code(self, filename):
        with open(filename, 'r') as file:
            code = file.read()
        
        if code == '':
            raise Exception("File is empty")
        
        return code
            
    def execute_check(self, title_slug, filename):
        question = getQuestionDetail(title_slug)
        self.params = {"lang": "python3",
                       "question_id": question.question_id,
                       "typed_code": self.load_code(filename),
                       "data_input": question.sample_test_case}
        
        # Interpret solution
        response = requests.post(url=self.interpret_url,
                                 headers=self.config.headers,
                                 json=self.params,
                                 cookies=self.config.cookies)
        self.runcode = response.json()['interpret_id']
        
        response = requests.get(url=self.runcode_check_url,
                            headers=self.config.headers,
                            cookies=self.config.cookies)
    
        while response.json().get('state') == 'STARTED' or response.json().get('state') == 'PENDING':
            response = requests.get(url=self.runcode_check_url,
                                    headers=self.config.headers,
                                    cookies=self.config.cookies)
        self.show_check_info(response.json())
    
    def show_check_info(self, response):
        if response.get('run_success'):
            print(f"Runtime: {response.get('status_runtime')}")
            print(f"Answer: {response.get('correct_answer')}")
            print(f"Expected: {response.get('expected_code_answer')}")
            print(f"Got answer: {response.get('code_answer')}")
        else:
            print(f"Exception: {response.get('status_msg')}")
            
    def execute_submission(self, title_slug, filename):
        # In similar way execute clicking submit button on the leetcode website
        question = getQuestionDetail(title_slug)
        self.params = {"lang": "python3",
                       "question_id": question.question_id,
                       "typed_code": self.load_code(filename)}

        # Submit solution
        response = requests.post(url=self.submit_url,
                                 headers=self.config.headers,
                                 json=self.params,
                                 cookies=self.config.cookies)
        self.submission_id = response.json()['submission_id']
        
        response = requests.get(url=self.submit_check_url,
                            headers=self.config.headers,
                            cookies=self.config.cookies)
    
        while response.json().get('state') == 'STARTED' or response.json().get('state') == 'PENDING':
            response = requests.get(url=self.submit_check_url,
                                    headers=self.config.headers,
                                    cookies=self.config.cookies)
        self.show_submission_info(response.json())
        
    def show_submission_info(self, response):
        if response.get('run_success'):
            print(f"Status: {response.get('status_msg')}")
            print(f"Runtime: {response.get('status_runtime')}")

            
            print(f"Runtime: {response.get('runtime_percentile')}")
            print(f"Memory: {response.get('memory_percentile')}")            
        else:
            print(f"Exception: {response.get('status_msg')}")