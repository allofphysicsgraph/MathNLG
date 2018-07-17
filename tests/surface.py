from unittest import TestCase, skip
from paramunittest import parametrized

from nlg import surfaceSymbol, surfaceFunction, surfaceStatement, surfaceStatementSingle

tests_symbol = [
    {
        'test': {},
        'data': {
            'representation': 'c',
            'type': 'real',
            'kind': 'constant'
        },
        'expected': '$c$ is a real constant'
    }
]

tests_function = [
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': 'real',
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'function': ['f'],
                    'representation': ['y'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': None,
            'symbols': []
        },
        'expected': '$f(x, y)$ is a real function where $x$ is a real variable and $y$ is a real variable'
    },
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': 'real',
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': None,
            'symbols': []
        },
        'expected': '$f(x, y)$ is a real function where $x$ and $y$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f', 'g'],
            'type': 'real',
            'dependencies': [
                {
                    'function': ['f', 'g'],
                    'representation': ['x', 'y'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': None,
            'symbols': []
        },
        'expected': '$f(x, y)$ and $g(x, y)$ are real functions where $x$ and $y$ are real variables'
    },
    {
        'test': {'disabled': True},
        'data': {
            'representation': ['f', 'g'],
            'type': 'real',
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'function': ['g'],
                    'representation': ['z'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': None,
            'symbols': []
        },
        'expected': '$f(x, y)$ and $g(z)$ are real functions where $x$, $y$ and $z$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': 'real',
            'dependencies': [
                {
                    'function': 'f',
                    'representation': ['x', 'y', 'z'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': None,
            'symbols': []
        },
        'expected': '$f(x, y, z)$ is a real function where $x$, $y$ and $z$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': 'real',
            'dependencies': [
                {
                    'function': 'f',
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': {
                'f': [
                    {'from': 'a', 'is': ['clean'], 'to': 'b'}
                ]
            },
            'symbols': [
                {
                    'representation': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant'
                }
            ]
        },
        'expected': '$f(x)$ is a real function such that $f(x)$ is clean from $a$ to $b$ where $x$ is a real variable and $a$ and $b$ are real constants'
    },
    {
        'test': {'disabled': True},
        'data': {
            'representation': ['f', 'g'],
            'type': 'real',
            'dependencies': [
                {
                    'function': ['f', 'g'],
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ],
            'statements': {
                'f': [
                    {'from': 'a', 'is': ['clean'], 'to': 'b'}
                ]
            },
            'symbols': [
                {
                    'representation': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant'
                }
            ]
        },
        'expected': '$f(x)$ and $g(x)$ are a real functions such that $f(x)$ is clean from $a$ to $b$ where $x$ is a real variable and $a$ and $b$ are real constants'
    }
]

tests_statement = [
    {
        'test': {},
        'func': {
            'f': 'f(x)'
        },
        'data': {
            'f': [
                {'from': 'a', 'is': ['clean'], 'to': 'b'}
            ]
        },
        'expected': 'such that $f(x)$ is clean from $a$ to $b$'
    },
    {
        'test': {},
        'func': {
            'f': 'f(x)'
        },
        'data': {
            'f': [
                {'at': 'a', 'is': ['broken']}
            ]
        },
        'expected': 'such that $f(x)$ is broken at $a$'
    },
    {
        'test': {},
        'func': {
            'f': 'f(x)'
        },
        'data': {
            'f': [
                {'from': 'a', 'is': ['clean'], 'to': 'b'},
                {'from': 'c', 'is': ['marvelous'], 'to': 'd'}
            ]
        },
        'expected': 'such that $f(x)$ is clean from $a$ to $b$ and marvelous from $c$ to $d$'
    },
    {
        'test': {},
        'func': {
            'f': 'f(x)'
        },
        'data': {
            'f': [
                {'from': 'a', 'is': ['clean'], 'to': 'b'},
                {'at': 'c', 'is': ['marvelous']},
                {'from': 'm', 'is': ['decent'], 'to': 'n'}
            ]
        },
        'expected': 'such that $f(x)$ is clean from $a$ to $b$, marvelous at $c$ and decent from $m$ to $n$'
    }
]

@parametrized(*tests_symbol)
class SymbolTest(TestCase) :
    def testSymbol(self) :
        if 'disabled' in self.test.keys() :
            if self.test['disabled'] :
                return skip('test disabled')
        output = surfaceSymbol(self.data)
        self.assertEqual(output, self.expected)
    def setParameters(self, test, data, expected):
        self.test = test
        self.data = data
        self.expected = expected

@parametrized(*tests_function)
class FunctionTest(TestCase) :
    def testFunction(self) :
        if 'disabled' in self.test.keys() :
            if self.test['disabled'] :
                return skip('test disabled')
        output = surfaceFunction(self.data)
        self.assertEqual(output, self.expected)
    def setParameters(self, test, data, expected):
        self.test = test
        self.data = data
        self.expected = expected

@parametrized(*tests_statement)
class StatementTest(TestCase) :
    def testStatement(self) :
        output = surfaceStatement(self.func, self.data)
        self.assertEqual(output, self.expected)
    def setParameters(self, test, func, data, expected):
        self.test = test
        self.func = func
        self.data = data
        self.expected = expected

class StatementSingleTest(TestCase) :
    def testSingle1(self) :
        input = {
            'is': ['clean'],
            'from': 'a',
            'to': 'b'
        }
        output = surfaceStatementSingle(input)
        expected = 'clean from $a$ to $b$'
        self.assertEqual(output, expected)
    def testSingle2(self) :
        input = {
            'is': ['clean'],
            'at': 'a'
        }
        output = surfaceStatementSingle(input)
        expected = 'clean at $a$'
        self.assertEqual(output, expected)
