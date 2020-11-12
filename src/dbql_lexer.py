from pyformlang.cfg import Terminal

KEYWORDS = [
    'connect',
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
    'final',
    'term',
    'var',
    'filter',
    'sat',
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