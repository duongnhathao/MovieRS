
import json

with open('data.json') as json_file:
    data = json.load(json_file)

File_name = data["filename"]
Min = data["min"]
direct = data["direct"]
if(data["row"]):
    limit_row = data["row"]
else:
    limit_row = ''
