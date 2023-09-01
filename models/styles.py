from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich import print
import rich

class LeetTable(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = rich.box.ROUNDED
        self.header_style = Style(color='blue', bold=True)
        self.width = 100
        
