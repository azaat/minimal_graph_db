grammar DbQlGrammar;

script : (stmt ';')* EOF ;

stmt : CONNECT STRING
     | SELECT target FROM graph
     | DEFINE pattern AS STRING
     ;

graph : graph_t
      | graph_t INTERSECT graph
      ;

graph_t : QUERY pattern
        | NAME STRING
        | LBR graph RBR
        | START_AND_FINAL LBR vertices COMMA vertices RBR OF graph
        ;

vertices : SET LBR set_expr RBR
         | RANGE LBR INT COMMA INT RBR
         | /* epsilon */
         ;

set_expr : (INT COMMA)* INT ;

pattern : concat_pattern ALT pattern
        | concat_pattern
        ;

concat_pattern : pattern_t CONCAT concat_pattern
               | pattern_t
               ;

pattern_t : pattern_t OPT
          | pattern_t PLUS
          | pattern_t STAR
          | pattern_val
          | LBR pattern RBR
          | EPS
          ;

pattern_val : VAR LBR STRING RBR
            | TERM LBR STRING RBR
            ;

target : edges
       | COUNT edges
       ;

edges : EDGES
      | FILTER edges WITH predicate
      ;

predicate : LBR vertname COMMA edgename COMMA vertname RBR SATISFIES bool_expr
          ;

vertname : VARNAME ;

edgename : VARNAME ;

bool_expr : bool_expr_and OR bool_expr
         | bool_expr_and
         ;

bool_expr_and : bool_expr_t AND bool_expr_and
             | bool_expr_t
             ;

bool_expr_t : NOT bool_term | bool_term ;

bool_term : LABEL_IS LBR STRING RBR
          | IS_START LBR vertname RBR
          | IS_FINAL LBR vertname RBR
          | LBR bool_expr RBR
          ;

NOT : 'not' ;
AND : 'and' ;
OR : 'or' ;
LABEL_IS : 'labelIs' ;
IS_START : 'isStart' ;
IS_FINAL : 'isFinal' ;
LBR : '(' ;
RBR : ')' ;
COMMA : ',' ;
DEFINE : 'define' ;
AS : 'as' ;
CONCAT : '.' | 'concat' ;
ALT : '|' | 'alt' ;
COUNT : 'count' ;
EDGES : 'edges' ;
FILTER : 'filter' ;
WITH : 'with' ;
SATISFIES : 'satisfies' ;
OPT : '?' | 'opt' ;
PLUS : '+' | 'plus' ;
STAR : '*' | 'star' ;
EPS : 'eps' ;
INTERSECT : 'intersect' ;
SELECT : 'select' ;
CONNECT : 'connect' ;
FROM : 'from' ;
QUERY : 'query' ;
NAME : 'name' ;
VAR : 'var' ;
TERM : 'term' ;
RANGE : 'range' ;
SET : 'set' ;
START_AND_FINAL : 'startAndFinal' ;
OF : 'of' ;
INT : [1-9][0-9]*
    | '0'
    ;
STRING : '"' ([a-zA-Z]|[0-9]|('\\' | '-' | '_' | ' ' | '/' | '.' | ',' | ':'))* '"' ;
VARNAME : [a-zA-Z] ([a-zA-Z]|[0-9])* ;
WS : [ \r\n\t]+ -> skip ;
