from typing import Optional
from rich.align import VerticalAlignMethod
from rich.console import JustifyMethod, OverflowMethod, RenderableType
from rich.table import Table
from rich.style import Style, StyleType
from rich.text import Text
from rich import print
import rich

difficulty_translate = {'Easy': '🟢 Easy', 
                        'Medium': '🟡 Medium',
                        'Hard': '🔴 Hard'}

status_retranslate = {'Solved': '✅ Solved',
                      'Attempted': '🟡 Attempted',
                      'Not attempted': '❌ Not attempted'}

class LeetTable(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = rich.box.ROUNDED
        self.header_style = Style(color='blue', bold=True)
        self.width = 100
        
        self.difficulty_column_index = None
        self.status_column_index = None
    
    def add_column(self, header: RenderableType = "", footer: RenderableType = "", *, header_style: StyleType | None = None, footer_style: StyleType | None = None, style: StyleType | None = None, justify: JustifyMethod = "left", vertical: VerticalAlignMethod = "top", overflow: OverflowMethod = "ellipsis", width: int | None = None, min_width: int | None = None, max_width: int | None = None, ratio: int | None = None, no_wrap: bool = False) -> None:
        if header == 'Difficulty':
            self.difficulty_column_index = len(self.columns)
        elif header == 'Status':
            self.status_column_index = len(self.columns)
        return super().add_column(header, footer, header_style=header_style, footer_style=footer_style, style=style, justify=justify, vertical=vertical, overflow=overflow, width=width, min_width=min_width, max_width=max_width, ratio=ratio, no_wrap=no_wrap)

    def add_row(self, *renderables: RenderableType | None, style: StyleType | None = None, end_section: bool = False) -> None:
        if self.difficulty_column_index or self.status_column_index:
            renderables = list(renderables)
            if self.difficulty_column_index is not None:
                renderables[self.difficulty_column_index] = difficulty_translate[renderables[self.difficulty_column_index]]
            if self.status_column_index is not None:
                renderables[self.status_column_index] = status_retranslate[renderables[self.status_column_index]]
            renderables = tuple(renderables)
        return super().add_row(*renderables, style=style, end_section=end_section)