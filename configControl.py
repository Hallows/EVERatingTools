import json

def readConfig():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data

def updateConfig_dailyGoals(value):
    with open('config.json', 'r') as file:
        data = json.load(file)
    data['dailyGoals'] = value
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def updateConfig_updateSpeed(value):
    with open('config.json', 'r') as file:
        data = json.load(file)
    data['updateSpeed'] = value
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def updateConfig_language(value):
    with open('config.json', 'r') as file:
        data = json.load(file)
    data['language'] = value
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def updateConfig_hideAD(value):
    with open('config.json', 'r') as file:
        data = json.load(file)
    data['hideAD'] = value
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def updateConfig_hideProcessBar(value):
    with open('config.json', 'r') as file:
        data = json.load(file)
    data['hideProcessBar'] = value
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)