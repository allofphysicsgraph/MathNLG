import pprint
pp = pprint.PrettyPrinter(indent=4)

from lxml import etree
from sympy import sympify, latex

from nlg.linguistic import plural

def surfaceProperty(property, representations, symbols) :
    filtered = {}
    filtered['constants'] = surfaceFilter(representation, symbols['constants'])
    filtered['functions'] = surfaceFilter(representation, symbols['functions'])
    filtered['variables'] = surfaceFilter(representation, symbols['variables'])
    symbol = surfaceFinder(symbols)
    text = '$%s$' % sympy.latex(sympify(representation))
    print text

def surfaceStatementSingle(statement) :
    if set(['from', 'to']).issubset(set(statement.keys())) :
        return '%s from $%s$ to $%s$' % (statement['is'][0], statement['from'], statement['to'])
    if set(['at']).issubset(set(statement.keys())) :
        return '%s at $%s$' % (statement['is'][0], statement['at'])
    return ''

def aggregator(strings) :
    if len(strings) > 2 :
        return '%s and %s' % (', '.join(strings[0:-1]), strings[-1])
    elif len(strings) > 1 :
        return '%s and %s' % (strings[0], strings[1])
    return strings[0]

def surfaceStatement(fs, func, data) :
    aggr = []
    for f in fs :
        if f in data.keys() :
            frep = func[f]
            statements = data[f]
            compiled = [surfaceStatementSingle(statement) for statement in statements]
            aggregated = aggregator(compiled)
            aggr.append('$%s$ is %s' % (frep, aggregated))
    return 'such that %s' % (aggregator(aggr))

# type is real, natural, complex etc
# kind is variable or constant
def surfaceSymbol(data) :
    if len(data['representation']) > 1 :
        wrapped = ['$%s$' % (s) for s in data['representation']]
        return '%s are %s %s' % (aggregator(wrapped), data['type'], plural(data['kind']))
    else :
        return '$%s$ is a %s %s' % (data['representation'][0], data['type'], data['kind'])

def surfaceFunction(data) :
    acc = []
    acs = {}
    for dependency in data['dependencies'] :
        acc.append(surfaceSymbol(dependency))
        if type(dependency['representation'][0]) == list :
            acs += dependency['representation'][0]
        else :
            for f in dependency['function'] :
                if f not in acs.keys() :
                    acs[f] = []
                acs[f] += dependency['representation']
    for dependency in data['symbols'] :
        acc.append(surfaceSymbol(dependency))
    func = []
    freps = {}
    for f in data['representation'] :
        frep = '%s(%s)' % (f, ', '.join(acs[f]))
        func.append(frep)
        freps[f] = frep
    st = ''
    if data['statements'] is not None :
        st = ' %s' % (surfaceStatement(data['representation'], freps, data['statements']))
    if len(func) > 1 :
        wrapped = ['$%s$' % (s) for s in func]
        return '%s are %s functions%s where %s' % (aggregator(wrapped), data['type'], st, aggregator(acc))
    else :
        return '$%s$ is a %s function%s where %s' % (func[0], data['type'], st, aggregator(acc))

# accepts text specification ts
# returns surface text st
def surfaceRealiser(ts) :
    for definition in ts['definition'] :
        data = definition['data']
        text = ''
        if 'if' in data.keys() and 'then' in data.keys() :
            #data['then']['statements'][0]
            #print 'then %s lol' % ('something')
            pp.pprint(data)
    st = None
    # TODO
    return st
