import json

from jinja2 import Template
from nlg.surface import surfaceRealize

def menu(node, rendered, linguistic) :
    if 'surface' in node.keys() :
        id = node['surface']
        entry = rendered[id]
        return '<li><a href="#%s">%s</a></li>' % (entry['id'], entry['title'])
    if 'title' in node.keys() :
        id = node['title']
        all = linguistic[id]['noun'].capitalize()
        if 'children' in node.keys() :
            compiled = ''
            for child in node['children'] :
                build = menu(child, rendered, linguistic)
                compiled += build
            all += '<ul class="toc_list">%s</ul>' % (compiled)
        return '<li>%s</li>' % (all)

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

planner = {}
with open('data/plan.json', 'r') as file :
    raw = file.read()
    planner = parse(raw)

rendered = {}
for id in data['source'].keys() :
    entry = data['source'][id]
    meta = {
        'linguistic': linguistic['linguistic']
    }
    title = ''
    rendered[id] = {}
    if entry['category'] == 'definition' :
        title = 'Definition of %s' % linguistic['linguistic'][id]['noun']
    else :
        title = (linguistic['linguistic'][id]['noun']).capitalize()
    rendered[id] = {'title': title, 'id': id}
    if 'category' in entry.keys() :
        rendered[id]['content'] = surfaceRealize(entry, meta)

txt = ''
for key in rendered.keys() :
    entry = rendered[key]
    txt += '<h3 id="%s" class="nlg">%s</h3><p>%s</p><a href="#toc_container">Go to top</a><hr>' % (entry['id'], entry['title'], entry['content'])

toc = '<ul class="toc_list">%s</ul>' % menu(planner, rendered, linguistic['linguistic'])

html = ''
with open('templates/index.html', 'r') as file :
    html = Template(file.read()).render({'toc': toc, 'content': txt})

with open('docs/index.html', 'w') as file:
    file.write(html)
