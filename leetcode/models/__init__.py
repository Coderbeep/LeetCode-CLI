# Import the available models from models folder
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import rich
from dataclass_wizard import JSONWizard
from rich import print
from rich.console import Console
from rich.table import Table
from .styles import ALERT, LeetTable, SubmitEvaluation

console = Console()

from leetcode.content_markdown import LeetQuestionToSections
from leetcode.graphql_query import GraphQLQuery
from leetcode.template import QueryTemplate

from leetcode.models.graphql_get_question_detail import getQuestionDetail
from leetcode.models.graphql_problemset_question_list import \
    problemsetQuestionList
from leetcode.models.graphql_question_content import questionContent
from leetcode.models.graphql_question_info_table import questionInfoTable
from leetcode.models.graphql_question_of_today import questionOfToday
from leetcode.models.graphql_submission_details import submissionDetails
from leetcode.models.graphql_submission_list import submissionList
from leetcode.models.graphql_user_problems_solved import userProblemsSolved
from leetcode.models.problem_by_id_slug import problemInfo
from leetcode.models.submit import sendSubmission
