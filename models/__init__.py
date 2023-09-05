# Import the available models from models folder

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import sys
import rich
from dataclass_wizard import JSONWizard
from rich import print
from rich.table import Table

from content_markdown import LeetQuestionToSections
from graphql_query import GraphQLQuery
from template import QueryTemplate

from .styles import LeetTable


from models.graphql_problemset_question_list import problemsetQuestionList
from models.graphql_question_of_today import questionOfToday
from models.graphql_user_problems_solved import userProblemsSolved