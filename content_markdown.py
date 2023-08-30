from rich.markdown import Markdown
from rich.panel import Panel
from markdownify import markdownify
from rich import print
import os



""" Turns the HTML code of the LeetCode question to sections. Then each section is 
    altered to Markdown and later into the Rich Panel. 
    
    - self.sections (list) - list of HTML content splitted to sections 
    - self.panels (list) - contains Markdown content turned into Rich module's Panel """

class LeetQuestionToSections():
    def __init__(self, html: str):
        self.html = html
        
        self.sections = []
        self.panels = []
        self.__divide_into_sections()
        self.__sections_into_panels()
        
    def __add_breaks(self):
        # Add the breaks into the Examples section
        self.sections[1] = self.sections[1].replace('<strong>Output:</strong>', '<br><strong>Output:</strong>')
        self.sections[1] = self.sections[1].replace('<strong>Explanation:</strong>', '<br><strong>Explanation:</strong>')
        

    def __divide_into_sections(self):
        self.html = self.html.split('<p>&nbsp;</p>')
        for section in self.html:
            self.sections.append(section)
            
        self.__add_breaks()
    
    def __sections_into_panels(self):
        for section in self.sections:
            section = markdownify(section, strip=['pre'])
            panel = Panel(Markdown(section), width=80)
            self.panels.append(panel)
               
    def __remove_empty_lines(self, section) -> str:
        section = os.linesep.join([
        line for line in section.splitlines()
        if line.strip() != ''])
        return section

    def __getitem__(self, index) -> Panel:
        return self.panels[index]
    
content = """<p>You are given a <strong>0-indexed</strong> integer array <code>nums</code>. In one operation you can replace any element of the array with <strong>any two</strong> elements that <strong>sum</strong> to it.</p>
<ul>
	<li>For example, consider <code>nums = [5,6,7]</code>. In one operation, we can replace <code>nums[1]</code> with <code>2</code> and <code>4</code> and convert <code>nums</code> to <code>[5,2,4,7]</code>.</li>
</ul>

<p>Return <em>the minimum number of operations to make an array that is sorted in <strong>non-decreasing</strong> order</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,9,3]
<strong>Output:</strong> 2
<strong>Explanation:</strong> Here are the steps to sort the array in non-decreasing order:
- From [3,9,3], replace the 9 with 3 and 6 so the array becomes [3,3,6,3]
- From [3,3,6,3], replace the 6 with 3 and 3 so the array becomes [3,3,3,3,3]
There are 2 steps to sort the array in non-decreasing order. Therefore, we return 2.

</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2,3,4,5]
<strong>Output:</strong> 0
<strong>Explanation:</strong> The array is already in non-decreasing order. Therefore, we return 0. 
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>
"""

markdown = """ 
```
**Input:** nums = [3,9,3]
**Output:** 2
**Explanation:** Here are the steps to sort the array in non-decreasing order:
- From [3,9,3], replace the 9 with 3 and 6 so the array becomes [3,3,6,3]
- From [3,3,6,3], replace the 6 with 3 and 3 so the array becomes [3,3,3,3,3]
There are 2 steps to sort the array in non-decreasing order. Therefore, we return 2.
```"""
