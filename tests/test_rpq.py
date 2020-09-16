import os
from src.automaton import RegexAutomaton
from src.graph import LabelGraph
from src.rpq import perform_rpq
from rpq_test_data.test_conf import n_tests
DATA_DIR = 'tests/rpq_test_data'


def test_rpq():
    for i in range(n_tests):
        # read Regex from file
        regex_string = open(
            os.path.join(DATA_DIR, f'regex_{i}.txt'), 'r'
        ).read()
        regex_automaton = RegexAutomaton(regex_string)

        # read GrB matrix from file
        graph = LabelGraph().from_txt(os.path.join(DATA_DIR, f'graph_{i}.txt'))
        start_lst = list(range(graph.num_vert))
        end_lst = list(range(graph.num_vert))

        res_matrix = perform_rpq(graph, regex_automaton, start_lst, end_lst)
        reachability = set()
        with open(
            os.path.join(DATA_DIR, f'reachability_{i}.txt'), 'r'
        ) as f:
            for line in f:
                v, to = line.split(' ')
                reachability.add((int(v), int(to)))
        assert(res_matrix.nvals == len(reachability))       
        for v, to, _ in zip(*res_matrix.to_lists()):
            if res_matrix[v, to] is True:
                assert((v, to) in reachability)
            else:
                assert((v, to) not in reachability)