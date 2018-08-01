from unittest import TestCase, skip
from paramunittest import parametrized

from nlg.surface import aggregator, wrapper, surfaceApply, surfaceMeta, surfaceStatement, surfaceInputs, numerize, constraint, constraints

def skipTest(test) :
    if 'disabled' in test.keys() :
        return test['disabled']

tests_statement = [
    {
        'test': {},
        'data': {
            'function': ['f'],
            'is': ['continuous'],
            'of': {
                'symbol': 'x',
                'from': 'a',
                'to': 'c'
            }
        },
        'meta': {
            'f': '$f(x)$'
        },
        'expected': '$f(x)$ is continuous for all $x$ from $a$ to $c$'
    },
    {
        'test': {},
        'data': {
            'expression': {
                'operator': 'eq',
                'lhs': 'f(b)',
                'rhs': '0'
            },
            'forall': ['b']
        },
        'meta': {},
        'expected': '$$f(b) = 0$$ is true for all $b$'
    },
    {
        'test': {},
        'data': {
            'function': ['derivative(f(x), x, k)'],
            'is': ['continuous'],
            'of': {
                'symbol': 'x',
                'from': 'a',
                'to': 'b'
            },
            'forall': ['k']
        },
        'meta': {
            'derivative(f(x), x, k)': '$\\frac{d^k}{dx^k}f(x)$'
        },
        'expected': '$\\frac{d^k}{dx^k}f(x)$ is continuous for all $x$ from $a$ to $b$ and for all $k$'
    },
    {
        'test': {},
        'data': {
            'symbol': 'n',
            'is': ['even']
        },
        'meta': {},
        'expected': '$n$ is even'
    },
    {
        'test': {},
        'data': {
            'symbol': 'n',
            'is': ['even', 'positive']
        },
        'meta': {},
        'expected': '$n$ is even and positive'
    },
    {
        'test': {},
        'data': {
            'symbol': 'n',
            'is': ['even', 'positive', 'finite']
        },
        'meta': {},
        'expected': '$n$ is even, positive and finite'
    },
    {
        'test': {'disabled': True},
        'data': {},
        'meta': {},
        'expected': ''
    }
]

tests_symbolic = [
    {
        'test': {},
        'data': [
            {
                'symbols': ['f'],
                'type': 'real',
                'kind': 'function',
                'dependencies': ['x']
            }
        ],
        'meta': {
            'f': '$f(x)$'
        },
        'expected': {
            'surfaceInput': 'let $f(x)$ be a real function',
            'surfaceSymbol': '$f(x)$ is a real function'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['f', 'g'],
                'type': 'real',
                'kind': 'function',
                'dependencies': ['x']
            }
        ],
        'meta': {
            'f': '$f(x)$',
            'g': '$g(x)$'
        },
        'expected': {
            'surfaceInput': 'let $f(x)$ and $g(x)$ be real functions',
            'surfaceSymbol': '$f(x)$ and $g(x)$ are real functions'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['f'],
                'type': 'real',
                'kind': 'function',
                'dependencies': ['x']
            },
            {
                'symbols': ['g'],
                'type': 'complex',
                'kind': 'function',
                'dependencies': ['z']
            }
        ],
        'meta': {
            'f': '$f(x)$',
            'g': '$g(z)$'
        },
        'expected': {
            'surfaceInput': 'let $f(x)$ be a real function and let $g(z)$ be a complex function',
            'surfaceSymbol': '$f(x)$ is a real function and $g(z)$ is a complex function'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['f'],
                'type': 'real',
                'kind': 'function',
                'dependencies': ['x']
            },
            {
                'symbols': ['g', 'h'],
                'type': 'complex',
                'kind': 'function',
                'dependencies': ['z']
            }
        ],
        'meta': {
            'f': '$f(x)$',
            'g': '$g(z)$',
            'h': '$h(z)$'
        },
        'expected': {
            'surfaceInput': 'let $f(x)$ be a real function and let $g(z)$ and $h(z)$ be complex functions',
            'surfaceSymbol': '$f(x)$ is a real function and $g(z)$ and $h(z)$ are complex functions'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['x'],
                'type': 'real',
                'kind': 'variable'
            },
            {
                'symbols': ['a', 'b', 'c'],
                'type': 'real',
                'kind': 'constant',
                'constraints': [
                    {
                        'symbol': 'b',
                        'type': 'outside',
                        'lb': 'a',
                        'ub': 'c'
                    }
                ]
            }
        ],
        'meta': {},
        'expected': {
            'surfaceInput': 'let $x$ be a real variable and let $a$, $b$ and $c$ be real constants such that $b$ is not contained between $a$ and $c$',
            'surfaceSymbol': '$x$ is a real variable and $a$, $b$ and $c$ are real constants such that $b$ is not contained between $a$ and $c$'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['x'],
                'type': 'real',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': {
            'surfaceInput': 'let $x$ be a real variable',
            'surfaceSymbol': '$x$ is a real variable'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['x', 'y'],
                'type': 'real',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': {
            'surfaceInput': 'let $x$ and $y$ be real variables',
            'surfaceSymbol': '$x$ and $y$ are real variables'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['x', 'y', 'z'],
                'type': 'real',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': {
            'surfaceInput': 'let $x$, $y$ and $z$ be real variables',
            'surfaceSymbol': '$x$, $y$ and $z$ are real variables'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['x', 'y', 'z'],
                'type': 'real',
                'kind': 'variable'
            },
            {
                'symbols': ['a', 'b'],
                'type': 'complex',
                'kind': 'constant'
            }
        ],
        'meta': {},
        'expected': {
            'surfaceInput': 'let $x$, $y$ and $z$ be real variables and let $a$ and $b$ be complex constants',
            'surfaceSymbol': '$x$, $y$ and $z$ are real variables and $a$ and $b$ are complex constants'
        }
    },
    {
        'test': {},
        'data': [
            {
                'symbols': ['n', 'k'],
                'type': 'integer',
                'kind': 'constant',
                'assumptions': ['positive'],
                'constraints': [
                    {
                        'type': 'geq',
                        'lhs': 'k',
                        'rhs': 'n'
                    }
                ]
            }
        ],
        'meta': {},
        'expected': {
            'surfaceInput': 'let $n$ and $k$ be positives integer constants such that $k$ is greater or equal than $n$',
            'surfaceSymbol': '$n$ and $k$ are positives integer constants such that $k$ is greater or equal than $n$'
        }
    }
]

@parametrized(*tests_statement)
class StatementTest(TestCase) :
    def testStatement(self) :
        if skipTest(self.test) : return skip('test disabled')
        output = surfaceStatement(self.data, self.meta)
        self.assertEqual(output, self.expected)
    def setParameters(self, test, data, meta, expected):
        self.test = test
        self.data = data
        self.meta = meta
        self.expected = expected

@parametrized(*tests_symbolic)
class SymbolicTest(TestCase) :
    def testStatement(self) :
        if skipTest(self.test) : return skip('test disabled')
        outputI = surfaceInputs(self.data, self.meta, 'input')
        outputS = surfaceInputs(self.data, self.meta, 'symbol')
        self.assertEqual(outputI, self.expected['surfaceInput'])
        self.assertEqual(outputS, self.expected['surfaceSymbol'])
    def setParameters(self, test, data, meta, expected):
        self.test = test
        self.data = data
        self.meta = meta
        self.expected = expected

class OtherTest(TestCase) :
    def testAggregator1(self) :
        strings = ['a']
        output = aggregator(strings)
        expected = 'a'
        self.assertEqual(output, expected)
    def testAggregator2(self) :
        strings = ['a', 'b']
        output = aggregator(strings)
        expected = 'a and b'
        self.assertEqual(output, expected)
    def testAggregator3(self) :
        strings = ['a', 'b', 'c']
        output = aggregator(strings)
        expected = 'a, b and c'
        self.assertEqual(output, expected)
    def testAggregator4(self) :
        strings = ['a', 'b', 'c', 'd']
        output = aggregator(strings)
        expected = 'a, b, c and d'
        self.assertEqual(output, expected)
    def testWrapper(self) :
        strings = ['a', 'b', 'c']
        output = wrapper('$%s$', strings)
        expected = ['$a$', '$b$', '$c$']
        self.assertEqual(output, expected)
    def testApply(self) :
        def someFun(str, meh) :
            return '_%s' % str
        data = ['a', 'b', 'c']
        output = surfaceApply(data, {}, someFun)
        expected = ['_a', '_b', '_c']
        self.assertEqual(output, expected)
    def testApply(self) :
        meta = {
            'f': '$f(x)$'
        }
        self.assertEqual(surfaceMeta('f', meta), '$f(x)$')
        self.assertEqual(surfaceMeta('g', meta), 'g')
        self.assertEqual(surfaceMeta(['f', 'g'], meta), ['$f(x)$', 'g'])
    def testNumerize(self) :
        self.assertEqual(numerize('real', [1, 2]), 'reals')
        self.assertEqual(numerize('complex', [1, 2]), 'complex')
    def testContraint1(self) :
        data = {
            'type': 'geq',
            'lhs': ['a', 'b'],
            'rhs': ['c']
        }
        output = constraint(data, {})
        expected = '$a$ and $b$ are greater or equal than $c$'
        self.assertEqual(output, expected)
    def testContraint2(self) :
        data = {
            'type': 'geq',
            'lhs': ['a'],
            'rhs': ['b', 'c']
        }
        output = constraint(data, {})
        expected = '$a$ is greater or equal than $b$ and $c$'
        self.assertEqual(output, expected)
    def testContraint3(self) :
        data = {
            'symbol': 'b',
            'type': 'inside',
            'lb': 'a',
            'ub': 'c'
        }
        output = constraint(data, {})
        expected = '$b$ is contained between $a$ and $c$'
        self.assertEqual(output, expected)
