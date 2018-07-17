from nlg.linguistic import plural

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
