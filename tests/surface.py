from unittest import TestCase, skip
from paramunittest import parametrized

from nlg.surface import surfaceSymbol, surfaceFunction, surfaceStatement, surfaceStatementSingle, surfaceType

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
            'type': [
                {
                    'function': ['f'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x']
                },
                {
                    'function': ['f'],
                    'representation': ['y']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'representation': ['y'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y)$ is a real function where $x$ is a real variable and $y$ is a real variable'
    },
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': [
                {
                    'function': ['f'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x', 'y'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y)$ is a real function where $x$ and $y$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f', 'g'],
            'type': [
                {
                    'function': ['f', 'g'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f', 'g'],
                    'representation': ['x', 'y']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x', 'y'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y)$ and $g(x, y)$ are real functions where $x$ and $y$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f', 'g'],
            'type': [
                {
                    'function': ['f', 'g'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y']
                },
                {
                    'function': ['g'],
                    'representation': ['z']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x', 'y'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'representation': ['z'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y)$ and $g(z)$ are real functions where $x$ and $y$ are real variables and $z$ is a real variable'
    },
    {
        'test': {},
        'data': {
            'representation': ['f', 'g'],
            'type': [
                {
                    'function': ['f', 'g'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y']
                },
                {
                    'function': ['g'],
                    'representation': ['z']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x', 'y', 'z'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y)$ and $g(z)$ are real functions where $x$, $y$ and $z$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f', 'g', 'h'],
            'type': [
                {
                    'function': ['f', 'g'],
                    'type': 'real'
                },
                {
                    'function': ['h'],
                    'type': 'complex'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y']
                },
                {
                    'function': ['g', 'h'],
                    'representation': ['z']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x', 'y', 'z'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y)$ and $g(z)$ are real functions and $h(z)$ is a complex function where $x$, $y$ and $z$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': [
                {
                    'function': ['f'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x', 'y', 'z']
                }
            ],
            'statements': None,
            'symbols': [
                {
                    'representation': ['x', 'y', 'z'],
                    'type': 'real',
                    'kind': 'variable'
                }
            ]
        },
        'expected': '$f(x, y, z)$ is a real function where $x$, $y$ and $z$ are real variables'
    },
    {
        'test': {},
        'data': {
            'representation': ['f'],
            'type': [
                {
                    'function': ['f'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f'],
                    'representation': ['x']
                }
            ],
            'statements': {
                'f': [
                    {'from': 'a', 'is': ['clean'], 'to': 'b'}
                ]
            },
            'symbols': [
                {
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
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
        'test': {},
        'data': {
            'representation': ['f', 'g'],
            'type': [
                {
                    'function': ['f', 'g'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f', 'g'],
                    'representation': ['x']
                }
            ],
            'statements': {
                'f': [
                    {'from': 'a', 'is': ['clean'], 'to': 'b'}
                ]
            },
            'symbols': [
                {
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'representation': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant'
                }
            ]
        },
        'expected': '$f(x)$ and $g(x)$ are real functions such that $f(x)$ is clean from $a$ to $b$ where $x$ is a real variable and $a$ and $b$ are real constants'
    },
    {
        'test': {},
        'data': {
            'representation': ['f', 'g'],
            'type': [
                {
                    'function': ['f', 'g'],
                    'type': 'real'
                }
            ],
            'dependencies': [
                {
                    'function': ['f', 'g'],
                    'representation': ['x']
                }
            ],
            'statements': {
                'f': [
                    {'from': 'a', 'is': ['clean'], 'to': 'b'}
                ],
                'g': [
                    {'at': 'c', 'is': ['broken']}
                ]
            },
            'symbols': [
                {
                    'representation': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'representation': ['a', 'b', 'c'],
                    'type': 'real',
                    'kind': 'constant'
                }
            ]
        },
        'expected': '$f(x)$ and $g(x)$ are real functions such that $f(x)$ is clean from $a$ to $b$ and $g(x)$ is broken at $c$ where $x$ is a real variable and $a$, $b$ and $c$ are real constants'
    }
]

tests_statement = [
    {
        'test': {},
        'fs': ['f'],
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
        'fs': ['f'],
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
        'fs': ['f'],
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
        'fs': ['f'],
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
        output = surfaceStatement(self.fs, self.func, self.data)
        self.assertEqual(output, self.expected)
    def setParameters(self, test, fs, func, data, expected):
        self.test = test
        self.fs = fs
        self.func = func
        self.data = data
        self.expected = expected

class OtherTest(TestCase) :
    def testStatementSingle1(self) :
        input = {
            'is': ['clean'],
            'from': 'a',
            'to': 'b'
        }
        output = surfaceStatementSingle(input)
        expected = 'clean from $a$ to $b$'
        self.assertEqual(output, expected)
    def testStatementSingle2(self) :
        input = {
            'is': ['clean'],
            'at': 'a'
        }
        output = surfaceStatementSingle(input)
        expected = 'clean at $a$'
        self.assertEqual(output, expected)
    def testSurfaceType(self) :
        func = {
            'f': 'f(x)',
            'g': 'g(x)',
            'h': 'h(x)'
        }
        data = [
            {
                'function': ['f', 'g'],
                'type': 'real'
            },
            {
                'function': ['h'],
                'type': 'complex'
            }
        ]
        output = surfaceType(func, data)
        expected = '$f(x)$ and $g(x)$ are real functions and $h(x)$ is a complex function'
        self.assertEqual(output, expected)
