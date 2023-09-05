import requests
import pandas as pd
req = requests.get("https://leetcode.com/api/problems/algorithms/").json()


# create a dictionary of question ID and titleSlug for easy access
for x in req['stat_status_pairs']:
    question_id = x['stat']['question_id']
    question_title = x['stat']['question__title_slug']
    print(question_id, question_title)
