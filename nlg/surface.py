import pypatt

import pprint
pp = pprint.PrettyPrinter(indent=4)

from lxml import etree
from sympy import sympify, latex

def surfaceRealize(data) :
    meta = {}
    input = surfaceInputs(data['input'], meta, 'input')
    symbols = surfaceInputs(data['symbols'], meta, 'symbol')
    if 'definition' in data.keys() :
        statements1 = surfaceStatements(data['definition'][0], meta)
        statements2 = surfaceStatements(data['definition'][1], meta)
        return ('%s, saying that %s is equivalent of saying that %s where %s' % (input, statements1, statements2, symbols)).capitalize()
    if 'theorem' in data.keys() :
        statements1 = surfaceStatements(data['theorem']['if'], meta)
        statements2 = surfaceStatements(data['theorem']['then'], meta)
        return ('%s such that if %s then %s where %s' % (input, statements1, statements2, symbols)).capitalize()
    return '<unrecognized logic structure>'

def constraint(data, meta) :
    if data['type'] in ['geq', 'leq', 'eq', 'neq'] :
        op = {
            'geq': 'greater or equal than',
            'leq': 'lower or equal than',
            'neq': 'equal to',
            'eq': 'not equal to'
        }[data['type']]
        lhs = aggregator(wrapper('$%s$', data['lhs']))
        rhs = aggregator(wrapper('$%s$', data['rhs']))
        return '%s %s %s %s' % (lhs, isare(data['lhs']), op, rhs)
    if data['type'] in ['inside', 'outside'] :
        op = {
            'outside': 'not contained between',
            'inside': 'contained between'
        }[data['type']]
        what = aggregator(wrapper('$%s$', data['symbol']))
        lb = aggregator(wrapper('$%s$', data['lb']))
        ub = aggregator(wrapper('$%s$', data['ub']))
        return '%s %s %s %s and %s' % (what, isare(data['symbol']), op, lb, ub)
    return ''

def constraints(data, meta) :
    constr = []
    for c in data :
        constr.append(constraint(c, meta))
    return ' such that %s' % (aggregator(constr))

def assumptions(data, meta) :
    assump = []

def surfacePreSymbolic(data, meta) :
    what = []
    if data['kind'] == 'function' :
        dependencies = data['dependencies']
        for symbol in data['symbols'] :
            str = '$%s(%s)$' % (symbol, ', '.join(dependencies))
            what.append(str)
    else :
        what = wrapper('$%s$', data['symbols'])
    desc = state(data['type'], data['kind'], what)
    constr = ''
    if 'constraints' in data.keys() :
        constr = constraints(data['constraints'], meta)
    assump = ''
    if 'assumptions' in data.keys() :
        words = data['assumptions']
        if len(what) > 1 :
            words = [plural(assumption) for assumption in data['assumptions']]
        assump = '%s ' % aggregator(words)
    return what, assump, desc, constr

def surfaceInput(what, assump, desc, constr) :
    return 'let %s be %s%s%s' % (aggregator(what), assump, desc, constr)

def surfaceSymbol(what, assump, desc, constr) :
    return '%s %s %s%s%s' % (aggregator(what), isare(what), assump, desc, constr)

def surfaceStatement(data, meta) :
    forall = None
    if 'forall' in data.keys() :
        forall = aggregator(wrapper('$%s$', data['forall']))
    if 'expression' in data.keys() :
        expr = expression(data['expression'])
        if forall is None :
            return '%s is true' % (expr)
        return '%s is true for all %s' % (expr, forall)
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

def surfaceInputs(inputs, meta, style) :
    def generateInput(data, meta) :
        what, assump, desc, constr = surfacePreSymbolic(data, meta)
        return surfaceInput(what, assump, desc, constr)
    def generateSymbol(data, meta) :
        what, assump, desc, constr = surfacePreSymbolic(data, meta)
        return surfaceSymbol(what, assump, desc, constr)
    if style == 'input' :
        applied = surfaceApply(inputs, meta, generateInput)
        return aggregator(applied)
    applied = surfaceApply(inputs, meta, generateSymbol)
    return aggregator(applied)

def surfaceStatements(statements, meta) :
    output = [surfaceStatement(statement, meta) for statement in statements]
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
    elif len(strings) == 1 :
        return strings[0]
    return ''

def surfaceMeta(key, meta) :
    def metaMeta(key, meta) :
        if key in meta.keys() :
            return meta[key]
        return key
    if type(key) == list :
        return [metaMeta(e, meta) for e in key]
    return metaMeta(key, meta)

def isare(countable) :
    return 'are' if len(countable) > 1 else 'is'

def numerize(word, countable) :
    return plural(word) if len(countable) > 1 else word

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
