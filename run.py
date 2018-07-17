from lxml import etree
from sympy import Symbol, sympify

from nlg.document import documentPlanner
from nlg.microplanner import microplanner
from nlg.surface import surfaceRealiser

# get knowledge source from the source.xml file
ks = None
with open('source.xml', 'r') as file :
    xml = file.read()
    ks = etree.XML(xml)

# get document plan from the knowledge source
dp = documentPlanner(ks)

# get text specification from microplanner
ts = microplanner(dp)

# get surface text from surface realiser
st = surfaceRealiser(ts)

# print the output
print st
