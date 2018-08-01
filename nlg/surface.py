import pypatt

import pprint
pp = pprint.PrettyPrinter(indent=4)

from lxml import etree
from sympy import sympify, latex

'''
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

def surfaceType(func, data) :
    aggr = []
    for ftype in data :
        wrapped = ['$%s$' % (func[s]) for s in ftype['function']]
        compiled = ''
        if len(wrapped) > 1 :
            compiled = '%s are %s functions' % (aggregator(wrapped), ftype['type'])
        else :
            compiled = '%s is a %s function' % (wrapped[0], ftype['type'])
        aggr.append(compiled)
    return aggregator(aggr)

def surfaceFunction(data) :
    acc = []
    acs = {}
    for dependency in data['dependencies'] :
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
    return '%s%s where %s' % (surfaceType(freps, data['type']), st, aggregator(acc))

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
'''



def surfaceRealize(data) :
    meta = {}
    input = surfaceInput(data['input'], meta)
    symbols = surfaceSymbols(data['symbols'], meta)
    if 'definition' in data.keys() :
        statements1 = surfaceStatements(data['definition'][0], meta)
        statements2 = surfaceStatements(data['definition'][1], meta)
        return '%s saying that %s is equivalent of saying that %s where %s' % (input, statements1, statements2, symbols)
    if 'theorem' in data.keys() :
        statements1 = surfaceStatements(data['theorem']['if'], meta)
        statements2 = surfaceStatements(data['theorem']['then'], meta)
        return '%s, if %s then %s where %s' % (input, statements1, statements2, symbols)
    return '<unrecognized logic structure>'

def surfaceInput(data, meta) :
    what = []
    if data['kind'] == 'function' :
        dependencies = data['dependencies']
        for symbol in data['symbols'] :
            str = '$%s(%s)$' % (symbol, ', '.join(dependencies))
            what.append(str)
    else :
        what = data['symbols']
    desc = state(data['type'], data['kind'], what)
    return 'let %s be %s' % (aggregator(what), desc)

def surfaceStatement(data, meta) :
    forall = None
    if 'forall' in data.keys() :
        forall = aggregator(wrapper('$%s$', data['forall']))
    if 'expression' in data.keys() :
        expression = expression(data['expression'])
        if forall is None :
            return '%s is true' % (expression)
        return '%s is true for all %s' % (expression, forall)
    verb = 'is'
    options = ['adjective']
    description = aggregator(data['is'])
    if 'function' in data.keys() :
        if len(data['function']) > 1 :
            verb = 'are'
            options = ['adjective', 'plural']
        functions = aggregator(surfaceMeta(data['function'], meta))
        oflist = [surfaceForAll(data['of'], meta)]
        if forall is not None :
            oflist.append('for all %s' % forall)
        of = aggregator(oflist)
        return '%s %s %s %s' % (functions, verb, description, of)
    if 'symbol' in data.keys() :
        if len(data['symbol']) > 1 :
            verb = 'are'
            options = ['adjective', 'plural']
        symbol = aggregator(wrapper('$%s$', data['symbol']))
        return '%s %s %s' % (symbol, verb, description)
    return ''

def expression(data) :
    if data['operator'] == 'eq' :
        return '$$%s = %s$$' % (data['lhs'], data['rhs'])
    return '$$%s \%s %s$$' % (data['lhs'], data['operator'], data['rhs'])

def surfaceForAll(data, meta) :
    symbols = aggregator(data['symbol'])
    if set(['from', 'to']).issubset(set(data.keys())) :
        return 'for all $%s$ from $%s$ to $%s$' % (symbols, data['from'], data['to'])
    if 'at' in data.keys() :
        return 'for all $%s$ at $%s$' % (symbols, data['at'])

def surfaceInputs(inputs, meta) :
    applied = surfaceApply(inputs, meta, surfaceInput)
    return aggregator(applied)

def surfaceStatements(statements, meta) :
    input = [(statement, meta) for statement in statements]
    output = surfaceApply(input, surfaceStatement)
    return aggregator(output)

def surfaceSymbols(data, meta) :
    return ''

def surfaceApply(data, meta, function) :
    return [function(d, meta) for d in data]

def wrapper(pattern, elements) :
    return [pattern % (element) for element in elements]

def aggregator(strings) :
    if len(strings) > 2 :
        return '%s and %s' % (', '.join(strings[0:-1]), strings[-1])
    elif len(strings) > 1 :
        return '%s and %s' % (strings[0], strings[1])
    return strings[0]

def surfaceMeta(key, meta) :
    def metaMeta(key, meta) :
        if key in meta.keys() :
            return meta[key]
        return key
    if type(key) == list :
        return [metaMeta(e, meta) for e in key]
    return metaMeta(key, meta)

def numerize(word, countable) :
    if len(countable) > 1 :
        return plural(word)
    return word

def plural(word) :
    if word == 'complex' : return 'complex'
    return '%ss' % (word)

def state(adjective, noun, countable) :
    snoun = numerize(noun, countable)
    if len(countable) < 2 :
        return 'a %s %s' % (adjective, snoun)
    return '%s %s' % (adjective, snoun)

@pypatt.transform
def linguistic(word, options) :
    with match([word] + options):
        with ['girl'] :
            return 'girl'
        with ['support', 'adjective'] :
            return 'supported'
    return word
