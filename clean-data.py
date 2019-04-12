import re
with open('raw-script.txt', 'r') as file:
    data = file.read()
data = re.sub(r'\[.*?\]', '', data)