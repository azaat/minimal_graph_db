
from pyformlang.regular_expression import Regex
from pygraphblas import BOOL, Matrix
from pyformlang.finite_automaton import Symbol, State
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


class RegexAutomaton:
    def __init__(self, regex):
        enfa = Regex(regex).to_epsilon_nfa()
        self.dfa = enfa.to_deterministic()
        states = self.dfa.states
        vertices = range(len(states))
        self.vert_dict = dict(zip(states, vertices))
        self.num_vert = len(self.vert_dict)  
        self.start_states = [
            self.vert_dict[st] for st in self.dfa.start_states
        ]
        self.final_states = [
            self.vert_dict[st] for st in self.dfa.final_states
        ]

    def to_GrB_matrix(self):
        tr_f = self.dfa._transition_function
        edges = tr_f.get_edges()
        self.matrix_dict = {}
        for s, p, o in edges:
            if (p.value not in self.matrix_dict):
                self.matrix_dict[p.value] = Matrix.sparse(
                    BOOL, self.num_vert,  self.num_vert
                )

            self.matrix_dict[p.value][
                self.vert_dict[s], self.vert_dict[o]
            ] = True
        return self.matrix_dict


class MatrixAutomaton:
    def __init__(self, matrix, start_states, final_states):
        self.matrix = matrix
        self.start_states = start_states
        self.final_states = final_states

    def to_dfa(self):
        edges = list(zip(*self.matrix.to_lists()))

        dfa = DeterministicFiniteAutomaton()

        # Creation of the states
        state_vals = range(self.matrix.ncols)
        state_dict = {}
        for value in state_vals:
            state_dict[value] = State(value)
        for value in self.start_states:
            dfa.add_start_state(state_dict[value])
        for value in self.final_states:
            dfa.add_final_state(state_dict[value])

        # Create transitions
        for s, p, o in edges:
            dfa.add_transition(state_dict[s], Symbol(p), state_dict[o])

        return dfa
