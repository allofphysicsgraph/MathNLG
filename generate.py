import json

from jinja2 import Template
from nlg.surface import surfaceRealize

def parse(text) :
    try:
        return json.loads(text)
    except ValueError as e:
        raise ValueError('invalid json: %s' % (e))

data = {}
with open('data/source.json', 'r') as file :
    raw = file.read()
    data = parse(raw)

linguistic = {}
with open('data/linguistic.json', 'r') as file :
    raw = file.read()
    linguistic = parse(raw)

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
    output.append({'title': title, 'id': id, 'content': content})

txt = ''
toc = '<ul class="toc_list">'
for entry in output :
    txt += '<h3 id="%s" class="nlg">%s</h3><p>%s</p><a href="#toc_container">Go to top</a><hr>' % (entry['id'], entry['title'], entry['content'])
    toc += '<li><a href="#%s">%s</a></li>' % (entry['id'], entry['title'])
toc += '</ul>'

html = ''
with open('templates/index.html', 'r') as file :
    html = Template(file.read()).render({'toc': toc, 'content': txt})

with open('docs/index.html', 'w') as file:
    file.write(html)
