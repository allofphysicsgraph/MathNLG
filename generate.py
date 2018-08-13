import json

from jinja2 import Template
from nlg.surface import surfaceRealize

data = {}
with open('data/source.json', 'r') as file :
    raw = file.read()
    data = json.loads(raw)

linguistic = {}
with open('data/linguistic.json', 'r') as file :
    raw = file.read()
    linguistic = json.loads(raw)

output = []
for id in data['source'].keys() :
    entry = data['source'][id]
    meta = {
        'linguistic': linguistic['linguistic']
    }
    title = ''
    if entry['category'] == 'definition' :
        title = 'Definition of %s' % linguistic['linguistic'][id]['noun']
    else :
        title = (linguistic['linguistic'][id]['noun']).capitalize()
    content = surfaceRealize(entry, meta)
    output.append({'title': title, 'content': content})

txt = ''
for entry in output :
    txt += '<h3>%s</h3><p>%s</p>' % (entry['title'], entry['content'])

#print txt

html = ''
with open('templates/index.html', 'r') as file :
    html = Template(file.read()).render({'content': txt})

with open('docs/index.html', 'w') as file:
    file.write(html)
