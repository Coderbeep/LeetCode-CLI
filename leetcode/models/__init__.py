# Import the available models from models folder
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import sys
import rich
from dataclass_wizard import JSONWizard
from rich import print
from rich.table import Table
from rich.console import Console
console = Console()

from leetcode.content_markdown import LeetQuestionToSections
from leetcode.graphql_query import GraphQLQuery
from leetcode.template import QueryTemplate

from .styles import LeetTable
from .styles import ALERT

from models.graphql_question_info_table import questionInfoTable
from models.graphql_question_content import questionContent
from models.graphql_problemset_question_list import problemsetQuestionList
from models.graphql_question_of_today import questionOfToday
from models.graphql_user_problems_solved import userProblemsSolved
from models.problem_by_id_slug import problemByIDSlug