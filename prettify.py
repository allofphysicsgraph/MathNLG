import json

data = {}
with open('data/source.json', 'r') as file :
    raw = file.read()
    data = json.loads(raw)

prettified = json.dumps(data, indent=2)

with open('data/source.json', 'w') as file:
    file.write(prettified)
