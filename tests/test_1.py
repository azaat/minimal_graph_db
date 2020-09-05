import pytest
from pygraphblas import Matrix, semiring
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon

def test_matrix_mul():
    matrix_1 = Matrix.from_lists([0, 1, 2], [1, 2, 0], [3, 5, 1])
    matrix_2 = Matrix.from_lists([0, 1, 2], [1, 2, 0], [2, 1, 4])
    
    # matrix multiplication
    res = matrix_1.mxm(matrix_2)
    assert res.nrows == 3
    assert res.ncols == 3
    assert res.nvals == 3
    exp_res = Matrix.from_lists([0, 1, 2], [2, 0, 1], [3, 20, 2])
    assert res.iseq(exp_res)


def test_enfa_intersection():
    enfa0 = EpsilonNFA()
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state2)
    enfa0.add_transition(state0, symb_a, state0)
    enfa0.add_transition(state0, symb_b, state1)
    enfa0.add_transition(state1, symb_c, state2)

    enfa1 = EpsilonNFA()
    state3 = State(3)
    state4 = State(4)
    state5 = State(5)
    enfa1.add_start_state(state3)
    enfa1.add_final_state(state5)
    enfa1.add_transition(state3, symb_a, state4)
    enfa1.add_transition(state4, symb_b, state5)
    enfa1.add_transition(state5, symb_c, state5)
    
    # getting intersection
    enfa = enfa0 & enfa1

    assert not enfa.accepts([symb_b])
    assert not enfa.accepts([symb_a])
    assert not enfa.accepts([])
    assert not enfa.accepts([symb_a, symb_a, symb_b, symb_c])
    assert not enfa.accepts([symb_a, symb_b, symb_c, symb_c])
    assert enfa.accepts([symb_a, symb_b, symb_c])

