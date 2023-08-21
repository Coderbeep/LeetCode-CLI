import re
FILENAME = 'file.graphql'

class Parser():
    def __init__(self, filename):
        self.filename = filename
    
    def extract_query_names(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            query_names = []
            for line in file:
                if line.startswith('query '):
                    query_name = re.split(r'[(|)]', line)[0].split(' ')[1]
                    query_names.append(query_name)
        return query_names
    
    def extract_query(self, query_name):
        with open(self.filename, 'r', encoding='utf-8') as file:
            query = ''
            for line in file:
                if line.startswith('query ' + query_name):
                    query += line
                    break
            for line in file:
                if line.startswith('}'):
                    break
                query += line
        return query
    
parser = Parser(FILENAME)
query_names = parser.extract_query_names()

print(parser.extract_query(query_names[0]))

