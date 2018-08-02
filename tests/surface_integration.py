from unittest import TestCase, skip
from paramunittest import parametrized

from nlg.tools import diffFormat, skipTest, assertEqual
from nlg.surface import surfaceRealize



tests = [
    {
        'test': {},
        'data': {
            'id': 'support',
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['support'],
                        'of': {
                                'symbol': 'x',
                                'from': 'a',
                                'to': 'c'
                        }
                    }
                ],
                [
                    {
                        'expression': {
                                'operator': 'neq',
                                'lhs': 'f(b)',
                                'rhs': '0'
                            },
                            'forall': ['b']
                    }
                ]
            ],
            'symbols': [
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
                            'type': 'inside',
                            'lb': 'a',
                            'ub': 'c'
                        }
                    ]
                }
            ]
        },
        'expected': 'Let $f(x)$ be a real function, saying that $f(x)$ is supported from $a$ to $b$ is equivalent of saying that following equation is true for all $b$ $$f(b) \\neq 0$$ where $x$ is a real variable and $a$, $b$ and $c$ are real constants such that $b$ is contained between $a$ and $c$'
    },
    {
        'test': {},
        'data': {
            'id': 'compact_support',
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['compact_support'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'c'
                        }
                    }
                ],
                [
                    {
                        'function': 'f',
                        'is': ['support'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'c'
                        }
                    },
                    {
                        'expression': {
                            'operator': 'eq',
                            'lhs': 'f(b)',
                            'rhs': '0'
                        },
                        'forall': ['b']
                    }
                ]
            ],
            'symbols': [
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
            ]
        },
        'expected': 'Let $f(x)$ be a real function, saying that $f(x)$ is compactly supported from $a$ to $b$ is equivalent of saying that $f(x)$ is supported from $a$ to $b$ and following equation is true for all $b$ $$f(b) = 0$$ where $x$ is a real variable and $a$, $b$ and $c$ are real constants such that $b$ is not contained between $a$ and $c$'
    },
    {
        'test': {},
        'data': {
            'id': 'continuity_at_point',
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['continuous'],
                        'of': {
                            'symbol': 'x',
                            'at': 'c'
                        },
                        'forall': ['c']
                    }
                ],
                [
                    {
                        'expression': {
                            'operator': 'eq',
                            'lhs': 'limit(f, x, c)',
                            'rhs': 'f(c)'
                        }
                    }
                ]
            ],
            'symbols': [
                {
                    'symbols': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'symbols': ['c'],
                    'type': 'real',
                    'kind': 'constant'
                }
            ]
        },
        'expected': 'Let $f(x)$ be a real function, saying that $f(x)$ is continuous at $c$ is equivalent of saying that following equation is true $$limit(f, x, c) = f(c)$$ where $x$ is a real variable and $c$ is a real constant'
    },
    {
        'test': {},
        'data': {
            'id': 'continuity_over_interval',
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['continuous'],
                        'of': {
                            'symbol': 'x',
                            'at': 'a'
                        }
                    }
                ],
                [
                    {
                        'function': 'f',
                        'is': ['continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    }
                ]
            ],
            'symbols': [
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
                            'type': 'contained',
                            'lb': 'a',
                            'ub': 'c'
                        }
                    ]
                }
            ]
        },
        'expected': 'Let $f(x)$ be a real function, saying that $f(x)$ is continuous from $a$ to $c$ is equivalent of saying that $f(x)$ is continuous at $b$ for al $b$ where $a$, $b$ and $c$ are real constants such that $b$ is contained between $a$ and $c$'
    },
    {
        'test': {},
        'data': {
            'id': 'nth_order_continuous',
            'parameters': ['n'],
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                },
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
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    },
                    {
                        'function': 'derivative(f(x), x, k)',
                        'is': ['continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        },
                        'forall': ['k']
                    }
                ],
                [
                    {
                        'function': 'f',
                        'is': ['nth_order_continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    }
                ]
            ],
            'symbols': [
                {
                    'symbols': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'symbols': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant',
                    'constraints': [
                        {
                            'type': 'gt',
                            'lhs': 'a',
                            'rhs': 'b'
                        }
                    ]
                }
            ]
        },
        'expected': 'Let $f(x)$ be a real function and let $n$ and $k$ be a positives integer constants such that $n$ is greater or equal than $k$, if $f(x)$ and for all $k$ $\frac{d^k}{dx^k}f(x)$ are continuous from $a$ to $b$ then $f(x)$ is n\'th order continuous from $a$ to $b$ where $a$ and $b$ are real constants such that $b$ is strictly greater than $a$'
    },
    {
        'test': {},
        'data': {
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['nth_order_continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    },
                    {
                        'symbol': 'n',
                        'is': ['infinity']
                    }
                ],
                [
                    {
                        'function': 'f',
                        'is': ['infinite_order_continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    }
                ]
            ],
            'symbols': [
                {
                    'symbols': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'symbols': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant',
                    'constraints': [
                        {
                            'type': 'gt',
                            'lhs': 'a',
                            'rhs': 'b'
                        }
                    ]
                }
            ],
        },
        'expected': 'Let $f(x)$ be a real function, saying that $f(x)$ is nth order continuous from $a$ to $b$ and $n$ is infinite is equivalent of saying that $f(x)$ is infinite order continuous from $a$ to $b$ where $a$ and $b$ are real constants such that $b$ is strictly greater than $a$'
    },
    {
        'test': {},
        'data': {
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'definition': [
                [
                    {
                        'function': 'f',
                        'is': ['infinite_order_continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    }
                ],
                [
                    {
                        'function': 'f',
                        'is': ['smooth'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    }
                ]
            ],
            'symbols': [
                {
                    'symbols': ['x'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'symbols': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant',
                    'constraints': [
                        {
                            'type': 'gt',
                            'lhs': 'a',
                            'rhs': 'b'
                        }
                    ]
                }
            ]
        },
        'expected': 'Let $f(x)$ be a real function, saying that $f(x)$ is infinite order continuous from $a$ to $b$ is equivalent of saying that $f(x)$ is smooth from $a$ to $b$ where $a$ and $b$ are real constants such that $b$ is strictly greater than $a$'
    },
    {
        'test': {},
        'data': {
            'input': [
                {
                    'symbols': ['f'],
                    'type': 'real',
                    'kind': 'function',
                    'dependencies': ['x']
                }
            ],
            'theorem': {
                'if': [
                    {
                        'function': 'f',
                        'is': ['continuous'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    },
                    {
                        'function': 'h',
                        'is': ['support_compact'],
                        'of': {
                            'symbol': 'x',
                            'from': 'a',
                            'to': 'b'
                        }
                    },
                    {
                        'expression': {
                            'operator': 'eq',
                            'lhs': 'Integral(f(t)*h(t), (x, a, b))',
                            'rhs': '0'
                        }
                    }
                ],
                'then': [
                    {
                        'expression': {
                            'operator': 'eq',
                            'lhs': 'f(t)',
                            'rhs': '0'
                        }
                    }
                ]
            },
            'symbols': [
                {
                    'symbols': ['x', 't'],
                    'type': 'real',
                    'kind': 'variable'
                },
                {
                    'symbols': ['a', 'b'],
                    'type': 'real',
                    'kind': 'constant',
                    'constraints': [
                        {
                            'type': 'gt',
                            'lhs': 'a',
                            'rhs': 'b'
                        }
                    ]
                }
            ]
        },
        'expected': 'Let $f(x)$ and $h(x)$ be real functions, if $f(x)$ is continuous from $a$ to $b$ and $h(x)$ is compactly supported from $a$ to $b$ and following statement is true $$Integral(f(t)*h(t), (x, a, b))=0$$ then also following statement must be true $$f(t)=0$$ where $x$ and $t$ are real variables and $a$ and $b$ are real constants such that $b$ is strictly greater than $a$'
    }
]

@parametrized(*tests)
class IntegrationTest(TestCase) :
    def testIntegration(self) :
        if skipTest(self.test) : return skip('test disabled')
        output = surfaceRealize(self.data)
        assertEqual(self, output, self.expected)
    def setParameters(self, test, data, expected):
        self.test = test
        self.data = data
        self.expected = expected
