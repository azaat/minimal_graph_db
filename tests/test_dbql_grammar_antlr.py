import os
from src.antlr_utils import parse
from src.grammar_cnf import GrammarCNF
import pytest


@pytest.mark.parametrize("grammar", [GrammarCNF.from_txt("dbql_grammar.txt")])
@pytest.mark.parametrize("test_input, expected", [
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from query term("s")*|term("b")+.term("c")?;
        ''',
            True
    ),
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
        select edges from name "sparsegraph_256.txt" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
            select edges 
            from startAndFinal(set(1, 2, 3), set (4, 5, 6))
            of name "sparsegraph" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from startAndFinal(set(1, 2, 3), set (4, 5, 6)) of name "sparsegraph" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        select filter edges with 
            ( u, l, v ) satisfies isStart(u) and isFinal(v)
                    from name "sparsegraph" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        select filter edges with 
            ( u, l, v ) satisfies labelIs("ar") or (isStart(u) and isFinal(v)) 
                    from name "sparsegraph" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        select filter edges with 
            ( u, l, v ) satisfies labelIs("ar") or (isStart(u) and isFinal(v)) 
                    from name "sparsegraph.txt" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from query term("s")*|term("b")+.term("c")? ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from name "sparsegraph" intersect query term("a") alt term("b") ;
        ''',
            True
    ),
    # graph expression with multiple levels:
    (
            '''
        connect "home/db" ;
        select count edges
            from startAndFinal(set(1, 2, 3), set(4, 5, 6))
                of name "fullgraph" intersect query term("a") star concat term("b");
        ''',
            True
    ),
(
            '''
        connect "home/db" ;
        select count edges
            from startAndFinal(range(1, 3), set(4, 5, 6))
                of name "fullgraph" intersect query term("a") star concat term("b");
        ''',
            True
    ),
    # edge expressions with multiple levels:
    (
            '''
        connect "azat/home/db" ; 

        select count filter edges 
        with ( u, e, v ) satisfies not isStart(u) and isFinal(v)
            from name "worstcase" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        define 
            term("a").var("s").term("b").var("s")
        as "s" ;
        define
            term("a").var("s1").term("b")
        as "s1" ;
        select edges 
            from name "sparsegraph256.txt" ;
        ''',
            True
    ),
    (
            '''
        connect "azat/home/db" ; 
        define 
            term("a").var("s").term("b").var("s")
        as "s" ;
        select edges 
            from name "sparsegraph" 
                intersect query term("a") | term("b");
        ''',
            True
    ),
    # the rest are False test cases ( when grammar shouldn't accept )
    # mismatched brackets in pattern:
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from term("a")*.(term("b")?.var("s")+ ;
        ''',
            False
    ),
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from query term("a"*.term("b")?.var("s")+ ;
        ''',
            False
    ),
    # wrong data type in range:
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from startAndFinal ( range( "typo", 3 ), set(4, 5, 6) ) of name "sparsegraph" ;
        ''',
            False
    ),
    # wrong data type in set:
    (
            '''
        connect "azat/home/db" ; 
        select edges 
            from startAndFinal ( range(1, 3 ), set(typo, 5, 6)) of name "sparsegraph" ;
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
    ),
])
# tests graph DB query language
def test_grammar_antlr(test_input, expected, grammar):
    assert expected == parse(test_input)
