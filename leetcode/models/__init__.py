# Import the available models from models folder
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from leetcode.loader import Loader

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

from leetcode.models.graphql_get_question_detail import GetQuestionDetail
from leetcode.models.graphql_problemset_question_list import \
    ProblemsetQuestionList
from leetcode.models.graphql_question_content import QuestionContent
from leetcode.models.graphql_question_info_table import QuestionInfoTable
from leetcode.models.graphql_question_of_today import QuestionOfToday
from leetcode.models.graphql_submission_details import SubmissionDetails
from leetcode.models.graphql_submission_list import SubmissionList
from leetcode.models.graphql_user_problems_solved import UserProblemsSolved
from leetcode.models.problem_by_id_slug import ProblemInfo
from leetcode.models.submit import SendSubmission
