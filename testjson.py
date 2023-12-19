import json

json_file_name_input="C:/Users/e013230/Desktop/Python Script/req.json"
json_file_name="C:/Users/e013230/Desktop/Python Script/output.json"

try:
    with open(json_file_name) as output_file:
        existing_data = json.load(output_file)
        
except FileNotFoundError:
    existing_data = []

f=open(json_file_name_input)
for i in f.readlines():
    x=json.loads(i)
    existing_data.append(x)
    

with open(json_file_name, "w") as output_file:
        json.dump(existing_data,output_file,indent=2)

