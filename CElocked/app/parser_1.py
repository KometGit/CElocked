import json 

with open('./app/config/config.data.json', 'r') as f1:
    config = json.load(f1)

with open('./app/config/keys.data.json', 'r') as f2:
    keys = json.load(f2)

with open('./app/config/colors/theme.data.json', 'r') as f3:
    theme = json.load(f3)