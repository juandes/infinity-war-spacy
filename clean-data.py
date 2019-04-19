import re

with open('raw-script.txt', 'r') as file:
    data = file.read()
data = re.sub(r'\[.*?\]', '', data)
data = re.sub(r'\(.*?\)', '', data)
# data = re.sub(r'.*:', '', data)

with open("cleaned-script-subject.txt", "w") as file:
    print(data, file=file)