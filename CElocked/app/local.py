import json, tk

def saveData(dict : dict, window):
    with open('./app/config/data/latest.min.json', 'w') as file:
        data = {
            "latest.file": dict['current']
        }
        json.dump(data, file, indent=4)
    window.destroy()

def openData():
    with open('./app/config/data/latest.min.json', 'r') as file:
        dt = json.load(file)
        return dt['latest.file']
