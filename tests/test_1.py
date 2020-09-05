import pytest
from pygraphblas import Matrix
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon

def test_matrix_mul():
    matrix_1 = Matrix.from_lists([0, 1, 2], [1, 2, 0], [1, 2, 3])
    matrix_2 = Matrix.from_lists([0, 1, 2], [1, 2, 0], [2, 3, 4])
    res = matrix_1.mxm(matrix_2)
    assert res.nrows == 3
    assert res.ncols == 3
    assert res.nvals == 3
    exp_res = Matrix.from_lists([0, 1, 2], [2, 0, 1], [3, 8, 6])
    assert res.iseq(exp_res)


def test_enfa_intersection():
    enfa0 = EpsilonNFA()
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    enfa0.add_start_state(state0)
    enfa0.add_final_state(state2)
    enfa0.add_transition(state0, symb_a, state0)
    enfa0.add_transition(state0, Epsilon(), state1)
    enfa0.add_transition(state1, symb_b, state2)

    symb_a = Symbol("a")
    symb_b = Symbol("b")
    eps = Epsilon()
    enfa1 = EpsilonNFA()
    state0 = State(10)
    state1 = State(11)
    state2 = State(12)
    state3 = State(13)
    state4 = State(14)
    enfa1.add_start_state(state0)
    enfa1.add_final_state(state3)
    enfa1.add_final_state(state4)
    enfa1.add_transition(state0, eps, state1)
    enfa1.add_transition(state1, symb_a, state2)
    enfa1.add_transition(state2, eps, state3)
    enfa1.add_transition(state3, symb_b, state4)

    # getting intersection
    enfa = enfa0 & enfa1
    assert len(enfa.start_states) == 4
    assert len(enfa.final_states) == 2
    assert len(enfa.symbols) == 2
    assert enfa.accepts([symb_a, symb_b])
    assert not enfa.accepts([symb_b])
    assert not enfa.accepts([symb_a])
    assert not enfa.accepts([])
    assert not enfa.accepts([symb_a, symb_a, symb_b])

