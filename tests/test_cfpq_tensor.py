import os
from src.cfpq import cfpq_tensor_product
from src.grammar_cnf import GrammarCNF
from pyformlang.cfg import CFG
from src.graph import LabelGraph
from cfpq_test_helper import NUM_GRAPHS, TEST_GRAMMARS, DATA_DIR


def test_cfpq_empty_graph():
    brackets_cnf = GrammarCNF.from_text(
            TEST_GRAMMARS[0]
    )
    result = cfpq_tensor_product(LabelGraph(), brackets_cnf)
    expected = set()
    edges = set(LabelGraph.get_reachable(result))
    assert edges == expected


def test_cfpq_brackets():
    for i in range(NUM_GRAPHS):
        brackets_cnf = CFG.from_text(
            TEST_GRAMMARS[0]
        )

        for i in range(NUM_GRAPHS):
            graph = LabelGraph().from_txt(
                os.path.join(DATA_DIR, f'graph_{i}.txt')
            )
            result = cfpq_tensor_product(graph, brackets_cnf)

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
        g_2 = CFG.from_text(
            TEST_GRAMMARS[1]
        )

        for i in range(NUM_GRAPHS):
            graph = LabelGraph().from_txt(
                os.path.join(DATA_DIR, f'graph_{i}.txt')
            )
            result = cfpq_tensor_product(graph, g_2)

            expected = set()
            with open(
                os.path.join(DATA_DIR, f'expected_{1}_{i}.txt'), 'r'
            ) as f:
                for line in f:
                    v, to = line.split(' ')
                    expected.add((int(v), int(to)))

            edges = set(LabelGraph.get_reachable(result))
            assert edges == expected
