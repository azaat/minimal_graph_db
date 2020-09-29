import os
from src.grammar_cnf import GrammarCNF
from src.cfpq import perform_cfpq
from src.graph import LabelGraph

DATA_DIR = 'tests/cfpq_test_data'
NUM_TESTS = 1


def test_brackets():
    for i in range(NUM_TESTS):
        brackets_cnf = GrammarCNF.from_text(
            'S -> a S b S\nS -> '
        )
        graph = LabelGraph().from_txt(os.path.join(DATA_DIR, f'graph_{i}.txt'))
        result, start_sym = perform_cfpq(graph, brackets_cnf)

        expected = set()
        with open(
            os.path.join(DATA_DIR, f'expected_{i}.txt'), 'r'
        ) as f:
            for line in f:
                v, to = line.split(' ')
                expected.add((int(v), int(to)))

        edges = set(result.get_edges(start_sym))
        assert edges == expected
