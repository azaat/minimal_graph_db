import os
from collections import deque
from src.grammar_cnf import GrammarCNF
from src.graph import LabelGraph, RFA
from pygraphblas import Matrix, BOOL, semiring
from pyformlang.cfg import Terminal, CFG
from src.rpq import get_transitive_closure


def cfpq_matrix_mult(g: LabelGraph, cfg: GrammarCNF):
    num_vert = g.num_vert
    if (num_vert == 0):
        return Matrix.sparse(BOOL, num_vert, num_vert)
    result = LabelGraph()
    start_sym = cfg.start_symbol
    result.num_vert = num_vert
    for variable in cfg.variables:
        result.graph_dict[variable] = Matrix.sparse(BOOL, num_vert, num_vert)

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

    if cfg.generate_epsilon():
        for v in g.vertices:
            result.graph_dict[start_sym][v, v] = True
    
    matrix_changing = True
    with semiring.LOR_LAND_BOOL:
        while matrix_changing:
            matrix_changing = False
            for production in cfg.pair_productions:
                head = production.head
                body = production.body
                prev_nvals = result.graph_dict[head].nvals
                tmp = result.graph_dict[body[0]] @ result.graph_dict[body[1]]
                result.graph_dict[head] = result.graph_dict[head] + tmp
                if (prev_nvals != result.graph_dict[head].nvals):
                    matrix_changing = True


    return result.graph_dict[start_sym]    


def cfpq_hellings(g: LabelGraph, cfg: GrammarCNF):
    num_vert = g.num_vert
    start_sym = cfg.start_symbol
    result = LabelGraph()
    result.num_vert = num_vert
    m = deque()

    for variable in cfg.variables:
        result.graph_dict[variable] = Matrix.sparse(BOOL, num_vert, num_vert)

    if cfg.generate_epsilon():
        for v in range(num_vert):
            result.graph_dict[start_sym][v, v] = True
    
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

    for label in result.graph_dict:
        for i, j in result.get_edges(label):
            m.append((label, i, j))

    # 3rd step: cfpq on modified matrix
    while m:
        var, v, u = m.popleft()
        for var_left in result.graph_dict:
            for v_new, v_ in result.get_edges(var_left):
                if (v_ == v):
                    for production in cfg.pair_productions:
                        if (
                            production.body[1] == var
                            and production.body[0] == var_left
                        ):
                            if (v_new, u) not in result.get_edges(production.head):
                                result.graph_dict[production.head][v_new, u] = True
                                m.append((production.head, v_new, u))
        for var_right in result.graph_dict:
            for u_, u_new in result.get_edges(var_right):
                if (u_ == u):
                    for production in cfg.pair_productions:
                        if (
                            production.body[1] == var_right
                            and production.body[0] == var
                        ):
                            if (v, u_new) not in result.get_edges(production.head):
                                result.graph_dict[production.head][v, u_new] = True
                                m.append((production.head, v, u_new))
    return result.graph_dict[start_sym]


def cfpq_tensor_product(g: LabelGraph, cfg: GrammarCNF):
    rfa = RFA().from_cfg(cfg)
    # Resulting matrix initialization
    result = LabelGraph()
    result.num_vert = g.num_vert
    # Empty matrix case
    if (g.num_vert == 0):
        return Matrix.sparse(BOOL, g.num_vert, g.num_vert)
    result.graph_dict = {
        label: g.graph_dict[label].dup() for label in g.graph_dict
    }
    for label in rfa.graph_dict:
        if label not in result.graph_dict:
            result.graph_dict[label] = Matrix.sparse(BOOL, g.num_vert, g.num_vert)
    for term in cfg.terminals:
        if term.value not in result.graph_dict:
            result.graph_dict[term.value] = Matrix.sparse(BOOL, g.num_vert, g.num_vert)
    # Loops for epsilon productions
    for p in cfg.productions:
        if p.body == []:
            for v in g.vertices:
                result.graph_dict[p.head.value][v, v] = True

    matrix_changing = True

    tc = None
    while matrix_changing:
        matrix_changing = False
        tmp_graph_dict = {}
        num_vert = 0
        # Getting intersection
        for label in rfa.graph_dict:
            tmp_graph_dict[label] = result.graph_dict[label].kronecker(
                rfa.graph_dict[label]
            )
            if num_vert == 0:
                num_vert = tmp_graph_dict[label].ncols
        # To GrB matrix
        tmp = LabelGraph()
        tmp.graph_dict = tmp_graph_dict
        tmp.num_vert = num_vert
        intersection = tmp.to_GrB_matrix()

        # Transitive closure
        old_nvals = 0 if tc is None else tc.nvals
        tc = get_transitive_closure(intersection)

        for s, o in LabelGraph.get_reachable(tc):
            # Get coordinates
            s_m, s_rfa = s // rfa.num_vert, s % rfa.num_vert
            o_m, o_rfa = o // rfa.num_vert, o % rfa.num_vert

            if s_rfa in rfa.start_states and o_rfa in rfa.final_states:
                label = rfa.var_by_vertices[(s_rfa, o_rfa)]
                result.graph_dict[label][s_m, o_m] = True
        if old_nvals != tc.nvals:
            matrix_changing = True
    
    return result.graph_dict[cfg.start_symbol.value]
