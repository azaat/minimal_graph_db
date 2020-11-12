from pyformlang.cfg import Terminal

KEYWORDS = [
    'connect',
    'concat'
    'select',
    'intersect',
    'from',
    'query',
    'name',
    'or',
    'and',
    'not',
    'is',
    'start',
    'star'
    'alt'
    'opt',
    'plus',
    'ptEps'
    'final',
    'term',
    'startAndFinal'
    'var',
    'filter',
    'satisfies',
    'count',
    'with'
]

def get_lex(word):
    lexems = []
    
    for lex in word.split():
        if lex in KEYWORDS:
            lexems.append(Terminal(lex))
        else:
            # Encountered string or int
            lexems.extend([Terminal(sym) for sym in lex])
    return lexems