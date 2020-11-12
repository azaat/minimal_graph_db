from src.grammar_cnf import GrammarCNF
from src.dbql_lexer import get_lex
import pytest
@pytest.mark.parametrize("test_input, expected", [
    (
        '''
        connect azat/home/db ; 
        connect azat ;
        ''', 
        True
    ),
    ('connect "azat/home/db" ;', True),
    ("__", False)
])

def test_grammar_cyk(test_input, expected):
    cnf = GrammarCNF.from_txt("dbql_grammar.txt")
    lexems = get_lex(test_input)
    assert cnf.contains_lex(lexems) == expected