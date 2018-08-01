from unittest import TestCase, skip
from paramunittest import parametrized

from nlg.surface import aggregator, wrapper, surfaceApply, surfaceMeta, surfaceStatement, surfaceInputs, numerize

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

tests_input = [
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
        'expected': 'let $f(x)$ be a real function'
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
        'expected': 'let $f(x)$ and $g(x)$ be real functions'
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
        'expected': 'let $f(x)$ be a real function and let $g(z)$ be a complex function'
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
        'expected': 'let $f(x)$ be a real function and let $g(z)$ and $h(z)$ be complex functions'
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
        'expected': 'let $f(x)$ be a real function and let $g(z)$ and $h(z)$ be complex functions'
    }
]

tests_symbols = [
    {
        'test': {},
        'data': [
            {
                'representation': ['x'],
                'type': 'real',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': 'x is a real variable'
    },
    {
        'test': {},
        'data': [
            {
                'representation': ['x', 'y'],
                'type': 'real',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': '$x$ and $y$ are real variables'
    },
    {
        'test': {},
        'data': [
            {
                'representation': ['x', 'y', 'z'],
                'type': 'real',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': '$x$, $y$ and $z$ are real variables'
    },
    {
        'test': {},
        'data': [
            {
                'representation': ['x', 'y', 'z'],
                'type': 'real',
                'kind': 'variable'
            },
            {
                'representation': ['a', 'b'],
                'type': 'complex',
                'kind': 'variable'
            }
        ],
        'meta': {},
        'expected': '$x$, $y$ and $z$ are real variables and $a$ and $b$ are complex constants'
    },
    {
        'test': {},
        'data': [
            {
                'representation': ['x'],
                'type': 'real',
                'kind': 'variable'
            },
            {
                'representation': ['a', 'b', 'c'],
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
        'expected': '$x$ is a real variable and $a$, $b$ and $c$ are real constants such that $b$ is not contained between $a$ and $c$'
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
        'expected': '$n$ and $k$ are positives integer constants such that $n$ is greater or equal than $k$'
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

@parametrized(*tests_input)
class InputTest(TestCase) :
    def testStatement(self) :
        if skipTest(self.test) : return skip('test disabled')
        output = surfaceInputs(self.data, self.meta)
        self.assertEqual(output, self.expected)
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
