from src.grammar_cnf import GrammarCNF
from src.dbql_lexer import get_lex
import pytest
@pytest.mark.parametrize( "grammar", [GrammarCNF.from_txt( "dbql_grammar.txt" )] )
@pytest.mark.parametrize( "test_input, expected", [
    ( 
        '''
        select edges from name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select edges from name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
            select edges 
            from startAndFinal ( set 1 2 3, set 4 5 6 )
            of name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from startAndFinal ( range ( 1, 3 ), set 4 5 6 ) of name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select filter edges with 
            ( u, l, v ) satisfies isStart u and isFinal v
                    from name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select filter edges with 
            ( u, l, v ) satisfies labelIs "ar" and ( isStart u and isFinal v ) 
                    from name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select filter edges with 
            ( u, l, v ) satisfies labelIs "ar" and isStart u 
                    from name "sparsegraph" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from query term "s" star alt term "b" plus concat term "c" opt;
        ''', 
        True
    ),    
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from query term "a" star alt ( term opt concat term "c" plus ) ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from name "sparsegraph" intersect query term "a" alt term "b" ;
        ''', 
        True
    ),
    # graph expression with multiple levels:
    (
        '''
        connect "home/db" ;
        select count edges
            from startAndFinal ( set 1 2 3, set 4 5 6 )
                of name "fullgraph" intersect query term "a" star term "b" ;
        ''',
        True
    ),
    # edge expressions with multiple levels:
    ( 
        '''
        connect "azat/home/db" ; 

        select count filter edges 
        with ( u, e, v ) satisfies not isStart u and isFinal v
            from name "worstcase" ;
        ''', 
        True
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        define 
            term "a" concat var "s" concat term "b" concat var "s"
        as "s" ;
        select edges 
            from name "sparsegraph" 
                intersect query term "a" alt term "b" ;
        ''', 
        True
    ),
    # the rest are False test cases ( when grammar shouldn't accept )
    # mismatched brackets in pattern:
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from query term "a" star alt ( term "a" opt concat term "c" plus ;
        ''', 
        False
    ),
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from query term "a" star alt ( term "a" opt concat term "c" plus ))) ;
        ''', 
        False
    ),
    # wrong data type in range:
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from startAndFinal ( range ( "typo", 3 ), set 4 5 6 ) of name "sparsegraph" ;
        ''', 
        False
    ),
    # wrong data type in set:
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from startAndFinal ( range ( 1, 3 ), set typo 5 6 ) of name "sparsegraph" ;
        ''', 
        False
    ),
    # not specified term or var in pattern:
    ( 
        '''
        connect "azat/home/db" ; 
        select edges 
            from query "a" star alt "a" opt concat "c" plus ;
        ''', 
        False
     )
] )


# tests graph DB query language with CYK
def test_grammar_cyk( test_input, expected, grammar ):
    lexems = get_lex( test_input )
    assert grammar.contains_lex( lexems ) == expected