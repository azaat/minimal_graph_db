import os
from src.cfpq import cfpq_matrix_mult
from src.grammar_cnf import GrammarCNF
from src.graph import LabelGraph

DATA_DIR = 'tests/cfpq_test_data'
NUM_GRAPHS = 2
TEST_GRAMMARS = [
    'S -> a S b S\nS -> ',
    'S -> S S\nS -> a b'
]


def test_cfpq_brackets():
    for i in range(NUM_GRAPHS):
        brackets_cnf = GrammarCNF.from_text(
            TEST_GRAMMARS[0]
        )

        for i in range(NUM_GRAPHS):
            graph = LabelGraph().from_txt(
                os.path.join(DATA_DIR, f'graph_{i}.txt')
            )
            result = cfpq_matrix_mult(graph, brackets_cnf)

            expected = set()
            with open(
                os.path.join(DATA_DIR, f'expected_{0}_{i}.txt'), 'r'
            ) as f:
                for line in f:
                    v, to = line.split(' ')
                    expected.add((int(v), int(to)))

            edges = set(LabelGraph.get_reachable(result))
            assert edges == expected


def test_cfpq_grammar_2():
    for i in range(NUM_GRAPHS):
        g_2 = GrammarCNF.from_text(
            TEST_GRAMMARS[1]
        )

        for i in range(NUM_GRAPHS):
            graph = LabelGraph().from_txt(
                os.path.join(DATA_DIR, f'graph_{i}.txt')
            )
            result = cfpq_matrix_mult(graph, g_2)

            expected = set()
            with open(
                os.path.join(DATA_DIR, f'expected_{1}_{i}.txt'), 'r'
            ) as f:
                for line in f:
                    v, to = line.split(' ')
                    expected.add((int(v), int(to)))

            edges = set(LabelGraph.get_reachable(result))
            assert edges == expected
