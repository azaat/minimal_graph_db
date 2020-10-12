import os
from src.grammar_cnf import GrammarCNF
from src.graph import LabelGraph
from pygraphblas import Matrix, BOOL
from pyformlang.cfg import Terminal


def cfpq_matrix_mult(graph: LabelGraph, grammar: GrammarCNF):
    num_vert = graph.num_vert
    result = LabelGraph()
    start_sym = grammar.start_symbol
    result.num_vert = num_vert
    for variable in grammar.variables:
        result.graph_dict[variable] = Matrix.sparse(BOOL, num_vert, num_vert)

    for label in graph.graph_dict:
        term = Terminal(label)
        for v_from, v_to in graph.get_edges(label):
            for production in grammar.productions:
                if (
                        len(production.body) == 1 and
                        production.body[0] == term
                ):
                    head = production.head
                    result.graph_dict[head][v_from, v_to] = True

    if grammar.generate_epsilon():
        for v in range(num_vert):
            result.graph_dict[start_sym][v, v] = True
    
    matrix_changing = True
    while matrix_changing:
        matrix_changing = False
        for production in grammar.productions:
            head = production.head
            body = production.body
            # Looking for productions of the form N1 -> N2 N3
            if (len(body) == 2):
                prev_nvals = result.graph_dict[head].nvals
                result.graph_dict[head] += result.graph_dict[body[0]] @ result.graph_dict[body[1]]
                if (prev_nvals != result.graph_dict[head].nvals):
                    matrix_changing = True

    return result.graph_dict[start_sym]    


def cfpq_hellings(graph: LabelGraph, grammar: GrammarCNF):
    num_vert = graph.num_vert
    start_sym = grammar.start_symbol
    result = LabelGraph()
    result.num_vert = num_vert
    for variable in cfg.variables:
        result.graph_dict[variable] = Matrix.sparse(BOOL, num_vert, num_vert)

    # 1st step: changing the terminals on edges to the sets of variables
    for label in g.graph_dict:
        term = Terminal(label)
        result.graph_dict[term] = g.graph_dict[label].dup()
        for v_from, v_to in g.get_edges(label):
            for production in cfg.productions:
                if (
                        len(production.body) == 1 and
                        production.body[0] == term
                ):
                    head = production.head
                    result.graph_dict[head][v_from, v_to] = True

    # 2nd step: adding loops for epsilon rule
    if cfg.generate_epsilon():
        for v in range(num_vert):
            result.graph_dict[start_sym][v, v] = True

    # 3rd step: cfpq on modified matrix
    matrix_changing = True
    while matrix_changing:
        matrix_changing = False
        for production in cfg.productions:
            head = production.head
            body = production.body
            # Looking for productions of the form N1 -> N2 N3
            if (len(body) == 2):
                for i, m in result.get_edges(body[0]):
                    for k, j in result.get_edges(body[1]):
                        if (k == m):
                            if (i, j) not in result.get_edges(head):
                                matrix_changing = True
                                result.graph_dict[head][i, j] = True

    return result.graph_dict[start_sym]
