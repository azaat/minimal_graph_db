from src.grammar_cnf import GrammarCNF
from src.dbql_lexer import get_lex
import pytest
@pytest.mark.parametrize("grammar", [GrammarCNF.from_txt("dbql_grammar.txt")])
@pytest.mark.parametrize("test_input, expected", [
    (
        '''
        select edges from name sparsegraph ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        connect azat ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        select edges from name sparsegraph ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
            select edges 
            from startAndFinal ( set 1 2 3 , set 4 5 6 )
            of name sparsegraph ;
        ''', 
        True
    ),
        (
        '''
        connect azat/home/db ; 
        select edges 
            from startAndFinal ( range ( 1 , 3 ) , set 4 5 6 ) of name sparsegraph ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        select filter edges with 
            ( u , l , v ) satisfies isStart u and isFinal v
                    from name sparsegraph ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        select filter edges with 
            ( u , l , v ) satisfies labelIs ar and ( isStart u and isFinal v ) 
                    from name sparsegraph ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        select filter edges with 
            ( u , l , v ) satisfies labelIs ar and isStart u 
                    from name sparsegraph ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        select edges 
            from query var s star alt term b plus concat term c opt;
        ''', 
        True
    ),    
    (
        '''
        connect azat/home/db ; 
        select edges 
            from query term a star alt ( term opt concat term c plus ) ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        select edges 
            from name sparsegraph intersect query term a alt term b ;
        ''', 
        True
    ),
    (
        '''
        connect azat/home/db ; 
        define 
            term a concat var s concat term b concat var s
        as s ;
        select edges 
            from name sparsegraph intersect query term a alt term b ;
        ''', 
        True
    ),
    # the rest are False test cases (when grammar shouldn't accept)
    # mismatched brackets in pattern:
    (
        '''
        connect azat/home/db ; 
        select edges 
            from query term a star alt ( term a opt concat term c plus ;
        ''', 
        False
    ),
    # not specified term or var in pattern:
    (
        '''
        connect azat/home/db ; 
        select edges 
            from query a star alt a opt concat c plus ;
        ''', 
        False
    )
])



def test_grammar_cyk(test_input, expected, grammar):
    lexems = get_lex(test_input)
    assert grammar.contains_lex(lexems) == expected