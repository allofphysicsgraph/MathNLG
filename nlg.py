import pprint
pp = pprint.PrettyPrinter(indent=4)

from lxml import etree
from sympy import sympify, latex

def plural(word) :
    return {
        'function': 'functions',
        'variable': 'variables',
        'constant': 'constants',
        'real': 'reals'
    }[word]

def extractTag(tree, tag) :
    all = []
    for child in tree :
        if child.tag == tag :
            all.append(child)
    return all

def groupByRepresentation(parent) :
    output = {}
    output['statements'] = {}
    output['expressions'] = []
    for child in parent :
        if child['type'] == 'statement' :
            representation = child['representation'][0]
            if representation not in output['statements'].keys() :
                output['statements'][representation] = []
            filtered = {k:v for (k,v) in child.items() if k != 'representation'}
            output['statements'][representation].append(filtered)
        else :
            output['expressions'].append(child)
    return output

def microplanProperty(property, id, type) :
    # prepare the specification object and fill it out
    specification = {}
    specification['type'] = type
    approved = ['representation', 'is', 'of', 'gt', 'lt', 'geq', 'leq', 'eq', 'from', 'to', 'forall', 'at']
    #print "---"
    for child in property :
        if child.tag in approved :
            if child.tag not in specification.keys() :
                #print child.tag
                specification[child.tag] = []
            specification[child.tag].append(child.text)
    # validate input
    if 'representation' not in specification.keys() :
        #print etree.tostring(property)
        raise ValueError('representation field is mandatory, id: ' + id)
    if len(specification['representation']) > 1 :
        raise ValueError('each property can have only one representation, id: ' + id)
    return specification

def microplanExpression(expression, id, type) :
    # prepare the specification object and fill it out
    specification = {}
    specification['type'] = type
    approved = ['gt', 'lt', 'geq', 'leq', 'eq', 'neq']
    if expression[0].tag not in approved :
        raise ValueError('unsupported type of equation, id: ' + id)
    specification['type'] = expression[0].tag
    specification['lhs'] = None
    specification['rhs'] = None
    for child in expression[0] :
        specification[child.tag] = child.text
    return specification

def microplanExtractProperties(properties, id) :
    all = []
    for child in properties :
        if child.tag == 'property' :
            all.append(microplanProperty(child, id, 'statement'))
        if child.tag == 'expression' :
            all.append(microplanExpression(child, id, 'expression'))
    return all

# accepts knowledge source ks
# returns document plan dp
def documentPlanner(ks) :
    # validate input
    if ks.tag != 'source' :
        raise ValueError('Document planner expects root of knowledge source')
    # document plan
    dp = {}
    dp['definition'] = []
    for child in ks :
        dp[child.tag].append(child)
    return dp

# accepts document plan dp
# returns text specification ts
def microplanner(dp) :
    ts = {}
    ts['definition'] = []
    # fill out the data
    for definition in dp['definition'] :
        construct = {}
        if definition.attrib['type'] == 'implication' :
            id = definition.attrib['id']
            # implication object structure
            construct['if'] = []
            construct['then'] = []
            # fill out the data
            for child in definition :
                construct[child.tag] = microplanExtractProperties(child, id)
            obj = {}
            obj['data'] = construct
            obj['id'] = id
            ts['definition'].append(obj)
    # aggregate
    for definition in ts['definition'] :
        # symbols
        construct = {}
        construct['functions'] = []
        construct['variables'] = []
        construct['constants'] = []
        #print symbols
        # get functions
        for symbol in definition['data']['symbols'] :
            symbolic = {}
            symbolic['representation'] = symbol['representation']
            if 'real' in symbol['is'] :
                symbolic['type'] = 'real'
            if 'function' in symbol['is'] :
                symbolic['of'] = symbol['of']
                construct['functions'].append(symbolic)
            elif 'variable' in symbol['is'] :
                construct['variables'].append(symbolic)
            elif 'constant' in symbol['is'] :
                construct['constants'].append(symbolic)
        definition['data']['symbols'] = construct
        # group by representation
        definition['data']['if'] = groupByRepresentation(definition['data']['if'])
        definition['data']['then'] = groupByRepresentation(definition['data']['then'])
        #pp.pprint(definition)
    return ts

def surfaceFilter(representation, symbols) :
    filtered = []
    for symbol in enumerate(symbols) :
        if representation not in symbol['representaion'] :
            filtered.append(symbol)
    return filtered

def surfaceFinder(representation, symbols) :
    for symbol in enumerate(symbols) :
        if representation in symbol['representaion'] :
            return representaion

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

def surfaceStatement(func, data) :
    aggr = []
    for f, statements in data.iteritems() :
        compiled = [surfaceStatementSingle(statement) for statement in statements]
        aggregated = aggregator(compiled)
        aggr.append('$%s$ is %s' % (func[f], aggregated))
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
    for f in data['representation'] :
        frep = '%s(%s)' % (f, ', '.join(acs[f]))
        func.append(frep)
    st = ''
    if data['statements'] is not None :
        # TODO extend to multiple functions
        fnc = {data['representation'][0]: func[0]}
        st = ' %s' % (surfaceStatement(fnc, data['statements']))
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
