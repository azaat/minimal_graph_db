from pyformlang.cfg import Terminal

KEYWORDS = [
    'connect',
    'concat',
    'select',
    'intersect',
    'from',
    'query',
    'name',
    'set',
    'range',
    'edges',
    'or',
    'of',
    'and',
    'not',
    'isStart',
    'star',
    'alt',
    'opt',
    'plus',
    'ptEps',
    'isFinal',
    'labelIs',
    'define',
    'term',
    'startAndFinal',
    'var',
    'filter',
    'satisfies',
    'count',
    'with',
    'as'
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